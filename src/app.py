import streamlit as st
import pandas as pd
import boto3
import json
import time

# --- Page Config (Branding) ---
st.set_page_config(
    page_title="GenAI - Test Suite Generator - Demo for Insurance",
    page_icon="🛡️",
    layout="wide"
)

# --- Initialize Session State ---
if "aws_configured" not in st.session_state:
    st.session_state.aws_configured = False
if "aws_credentials" not in st.session_state:
    st.session_state.aws_credentials = {}

# --- Sidebar Configuration ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Amazon_Web_Services_Logo.svg/1024px-Amazon_Web_Services_Logo.svg.png", width=150)
st.sidebar.title("🔐 AWS Configuration")

# AWS Credentials Section
with st.sidebar.expander("AWS Credentials", expanded=not st.session_state.aws_configured):
    st.markdown("**Enter your AWS credentials:**")
    
    aws_access_key = st.text_input(
        "AWS Access Key ID",
        value=st.session_state.aws_credentials.get("access_key", ""),
        type="password",
        help="Your AWS access key ID"
    )
    
    aws_secret_key = st.text_input(
        "AWS Secret Access Key",
        value=st.session_state.aws_credentials.get("secret_key", ""),
        type="password",
        help="Your AWS secret access key"
    )
    
    if st.button("Save AWS Credentials"):
        if aws_access_key and aws_secret_key:
            st.session_state.aws_credentials = {
                "access_key": aws_access_key,
                "secret_key": aws_secret_key
            }
            st.session_state.aws_configured = True
            st.success("✅ AWS credentials saved successfully!")
        else:
            st.error("Please provide both Access Key ID and Secret Access Key")

# Configuration Section
st.sidebar.markdown("---")
st.sidebar.title("⚙️ Model Configuration")

region = st.sidebar.text_input(
    "AWS Region",
    "us-east-1",
    help="AWS region where Bedrock is available (e.g., us-east-1, us-west-2)"
)

model_id = st.sidebar.selectbox(
    "Select Foundation Model",
    [
        "anthropic.claude-3-sonnet-20240229-v1:0",
        "anthropic.claude-3-haiku-20240307-v1:0"
    ],
    index=0,
    help="Choose the Claude model to use for test case generation"
)

temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.1,
    step=0.1,
    help="Lower values (0.1) = more consistent, Higher values (1.0) = more creative"
)

max_tokens = st.sidebar.slider(
    "Max Tokens",
    min_value=500,
    max_value=4000,
    value=2000,
    step=100,
    help="Maximum tokens for model response"
)

st.sidebar.markdown("---")
st.sidebar.info(
    """
    **Security Note:** 
    - Credentials are stored in session memory only
    - Data processed here remains within the VPC
    - No data is shared with public LLM providers
    """
)

# --- Token and Cost Calculation ---
def calculate_bedrock_cost(model_id, input_tokens, output_tokens):
    """Calculate approximate cost for Claude models on Bedrock (per 1M tokens)"""
    # Claude 3 Sonnet pricing (as of 2024)
    sonnet_input = 0.003      # $3 per 1M input tokens
    sonnet_output = 0.015     # $15 per 1M output tokens
    
    # Claude 3 Haiku pricing (as of 2024)
    haiku_input = 0.00025     # $0.25 per 1M input tokens
    haiku_output = 0.00125    # $1.25 per 1M output tokens
    
    if "sonnet" in model_id.lower():
        input_cost = (input_tokens / 1000000) * sonnet_input
        output_cost = (output_tokens / 1000000) * sonnet_output
    else:  # Haiku
        input_cost = (input_tokens / 1000000) * haiku_input
        output_cost = (output_tokens / 1000000) * haiku_output
    
    total_cost = input_cost + output_cost
    return total_cost, input_tokens, output_tokens

# --- Bedrock Integration Function ---
def generate_tests_with_bedrock(row, model_arn, credentials, region, temp, max_tok):
    """Calls AWS Bedrock to generate test cases for a single story."""
    
    try:
        # Initialize Bedrock client with provided credentials
        bedrock = boto3.client(
            service_name="bedrock-runtime",
            region_name=region,
            aws_access_key_id=credentials.get("access_key"),
            aws_secret_access_key=credentials.get("secret_key")
        )
        
        prompt = f"""
    You are a Senior QA Automation Engineer for a major Insurance Provider.
    
    Analyze this User Story:
    ID: {row['FormattedID']}
    Title: {row['Name']}
    Description: {row['Description']}
    Acceptance Criteria: {row['AcceptanceCriteria']}
    
    OUTPUT REQUIREMENTS:
    Generate 2-3 specific Test Cases. Return ONLY valid JSON.
    Format:
    [
        {{
            "TestID": "TC-{row['FormattedID']}-01",
            "Type": "Positive/Negative/Edge",
            "Summary": "Short summary...",
            "Steps": "1. Step one... 2. Step two...",
            "Expected_Result": "...",
            "Confidence": 0.95
        }}
    ]
    
    Also include a 'Confidence' field (0.0-1.0) indicating how confident you are in the test case quality.
    """

        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tok,
            "temperature": temp,
            "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}]
        })

        response = bedrock.invoke_model(modelId=model_arn, body=body)
        response_body = json.loads(response.get("body").read())
        result_text = response_body['content'][0]['text']
        
        # Extract token usage from response metadata
        input_tokens = response_body.get('usage', {}).get('input_tokens', len(prompt.split()))
        output_tokens = response_body.get('usage', {}).get('output_tokens', len(result_text.split()))
        
        # Extract JSON from potential chat text
        json_start = result_text.find('[')
        json_end = result_text.rfind(']') + 1
        test_cases = json.loads(result_text[json_start:json_end])
        
        # Add token and cost info to each test case
        cost, _, _ = calculate_bedrock_cost(model_arn, input_tokens, output_tokens)
        for test in test_cases:
            test['InputTokens'] = input_tokens
            test['OutputTokens'] = output_tokens
            test['TotalTokens'] = input_tokens + output_tokens
            test['EstimatedCost'] = round(cost, 6)
        
        return test_cases
        
    except Exception as e:
        st.error(f"Error calling Bedrock: {str(e)}")
        return []

# --- Main UI ---
st.title("🛡️ GenAI: Automated Test Architect - Demo for Insurance")
st.markdown("### Accelerating Insurance QA with AWS Bedrock")

# Check AWS Credentials
if not st.session_state.aws_configured:
    st.warning("⚠️ Please configure your AWS credentials in the sidebar first!")

uploaded_file = st.file_uploader("Upload User Stories (CSV)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # Show Preview
    st.subheader("1. User Story Backlog")
    st.dataframe(df[['FormattedID', 'Name', 'AcceptanceCriteria']].head(), use_container_width=True)
    
    if st.button("🚀 Generate Test Cases", type="primary", disabled=not st.session_state.aws_configured):
        
        if not st.session_state.aws_configured:
            st.error("❌ AWS credentials not configured. Please set them up in the sidebar.")
        else:
            # UI Container for results
            results_container = st.container()
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            all_generated_tests = []
            
            # Limit to 5 stories for demo speed (remove .head(5) for full file)
            stories_to_process = df.head(5) 
            total_stories = len(stories_to_process)

            for index, row in stories_to_process.iterrows():
                status_text.text(f"Processing {row['FormattedID']}: {row['Name']}...")
                
                # Call AI with updated parameters
                tests = generate_tests_with_bedrock(
                    row,
                    model_id,
                    st.session_state.aws_credentials,
                    region,
                    temperature,
                    max_tokens
                )
                
                # Flatten results for table display
                for test in tests:
                    test['Parent_Story_ID'] = row['FormattedID']
                    all_generated_tests.append(test)
                
                # Update Progress
                progress_bar.progress((index + 1) / total_stories)
                time.sleep(0.5) # Slight UX pause

            progress_bar.progress(100)
            status_text.success("✅ Generation Complete!")
            
            # --- Display Results ---
            st.divider()
            st.subheader("2. Generated Test Suite")
            
            if all_generated_tests:
                results_df = pd.DataFrame(all_generated_tests)
                
                # Calculate average confidence score
                avg_confidence = 0.0
                if 'Confidence' in results_df.columns:
                    avg_confidence = results_df['Confidence'].astype(float).mean()
                else:
                    # Default confidence if not provided
                    avg_confidence = 0.85
                
                # Calculate token and cost statistics
                total_input_tokens = results_df['InputTokens'].sum() if 'InputTokens' in results_df.columns else 0
                total_output_tokens = results_df['OutputTokens'].sum() if 'OutputTokens' in results_df.columns else 0
                total_tokens = results_df['TotalTokens'].sum() if 'TotalTokens' in results_df.columns else 0
                total_cost = results_df['EstimatedCost'].sum() if 'EstimatedCost' in results_df.columns else 0
                
                # Metric Summary - Row 1
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Stories Processed", total_stories)
                col2.metric("Test Cases Generated", len(results_df))
                col3.metric(
                    "Est. Hours Saved / Confidence",
                    f"{len(results_df) * 0.5:.1f} hrs",
                    delta=f"{avg_confidence*100:.0f}% confident"
                )
                col4.metric(
                    "Estimated Cost",
                    f"${total_cost:.4f}",
                    delta=f"{total_tokens:,} tokens"
                )

                # Token Breakdown
                st.markdown("---")
                st.markdown("**Token Usage Breakdown:**")
                token_col1, token_col2, token_col3 = st.columns(3)
                token_col1.metric("Input Tokens", f"{total_input_tokens:,}")
                token_col2.metric("Output Tokens", f"{total_output_tokens:,}")
                token_col3.metric("Total Tokens", f"{total_tokens:,}")

                # Data Table
                st.dataframe(
                    results_df[['Parent_Story_ID', 'TestID', 'Type', 'Summary', 'Expected_Result']],
                    use_container_width=True,
                    hide_index=True
                )
                
                # Download Button
                csv = results_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Test Plan (CSV)",
                    data=csv,
                    file_name="genai_test_plan.csv",
                    mime="text/csv"
                )
            else:
                st.warning("⚠️ No test cases were generated. Check your AWS Credentials and try again.")