# InsureGenAI: Automated Test Suite Generator

A comprehensive Python solution for generating synthetic insurance test data and automatically creating intelligent test cases using AWS Bedrock and Claude AI models.

## 📋 Overview

This workspace contains two complementary projects:

1. **Test Data Generator** (`testdatagenerator.py`) - Generates realistic synthetic insurance user stories
2. **AI Test Case Generator** (`app.py`) - Transforms user stories into comprehensive test suites using Claude AI on AWS Bedrock

The combination enables end-to-end automation: generate test data → transform to user stories → auto-generate test cases with AI.

## ✨ Key Features

### Test Data Generator
- **Synthetic User Story Creation**: Generates realistic insurance user stories with unique IDs
- **Domain-Specific Content**: Uses insurance terminology, roles, and business scenarios
- **Acceptance Criteria**: Auto-generates 3-5 acceptance criteria per user story
- **CSV Export**: Saves data in CSV format for integration with testing tools

### AI Test Case Generator (app.py)
- **AWS Bedrock Integration**: Leverages Claude AI models for intelligent test generation
- **AWS Credentials Management**: Secure UI for managing AWS credentials
- **Configurable AI Parameters**: Adjust model selection, temperature, and token limits
- **Token & Cost Tracking**: Real-time monitoring of API usage and estimated costs
- **Confidence Scoring**: AI provides confidence metrics for generated test cases
- **Interactive Streamlit UI**: User-friendly web interface for test generation
- **CSV Export**: Download generated test plans for integration with test management tools

## 📁 Project Structure

```
testcasegenerator/
├── src/
│   ├── testdatagenerator.py          # Synthetic data generation script
│   ├── app.py                         # Streamlit UI for AI test generation
│   └── __pycache__/                   # Python cache files
├── output/                            # Generated output files
│   └── insurance_user_stories.csv     # Generated CSV output
├── docs/                              # Documentation
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Git ignore rules
└── README.md                          # This file
```

## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- AWS Account with Bedrock access
- AWS Access Key ID and Secret Access Key

### Setup

1. **Clone the repository**:
```bash
git clone <repository-url>
cd testcasegenerator
```

2. **Create a virtual environment**:
```bash
python3 -m venv .venv
source ./.venv/bin/activate  # On Windows: .\.venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## 💻 Usage

### Project 1: Test Data Generator

Generate synthetic insurance user stories:

```bash
cd src
python3 testdatagenerator.py
```

**Output:**
- Generates 500 user stories by default
- Displays preview in console
- Saves to `output/insurance_user_stories.csv`

**Customization:**
```python
# Generate different number of stories
df = generate_insurance_user_stories(num_records=1000)
```

### Project 2: AI Test Case Generator (app.py)

Run the interactive Streamlit application:

```bash
cd src
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

#### Using the Application

**Step 1: Configure AWS Credentials**
1. Expand "AWS Credentials" in the left sidebar
2. Enter your AWS Access Key ID and Secret Access Key
3. Click "Save AWS Credentials"

**Step 2: Configure Model Settings**
- **AWS Region**: Select region where Bedrock is available (default: us-east-1)
- **Foundation Model**: Choose between Claude 3 Sonnet or Haiku
- **Temperature**: Adjust creativity (0.0 = consistent, 1.0 = creative)
- **Max Tokens**: Set maximum response length (default: 2000)

**Step 3: Generate Test Cases**
1. Click "Upload User Stories (CSV)" and select your CSV file
2. Review the user story preview
3. Click "🚀 Generate Test Cases" button
4. Monitor real-time progress and token usage

**Step 4: Review Results**
- View metrics: Stories processed, test cases generated, hours saved, confidence score
- See token usage breakdown (input, output, total)
- Check estimated API costs
- Download test plan as CSV

## 📊 Generated Fields

### User Stories (testdatagenerator.py)

Each user story includes:
- **FormattedID**: Unique identifier (US00001, US00002, etc.)
- **Name**: User story in BDD format (As a..., I want..., so that...)
- **Description**: Detailed business requirement description
- **Notes**: Developer notes, edge cases, priority flags
- **AcceptanceCriteria**: 3-5 acceptance criteria

### Test Cases (app.py)

Each generated test case includes:
- **TestID**: Unique test case identifier
- **Type**: Test category (Positive, Negative, Edge)
- **Summary**: Short description of the test
- **Steps**: Detailed test execution steps
- **Expected_Result**: Expected outcome
- **Confidence**: AI confidence score (0.0-1.0)
- **InputTokens**: Tokens used for input
- **OutputTokens**: Tokens used for output
- **TotalTokens**: Combined token usage
- **EstimatedCost**: Approximate API cost for that test case

## 🔐 Security Considerations

- **Credential Storage**: AWS credentials are stored in session memory only
- **No Data Sharing**: All processing remains within your AWS VPC
- **Secure Input Fields**: Password-masked input for sensitive credentials
- **No Cloud Logging**: Data is not shared with public LLM providers

## 💰 Cost Optimization

The application provides real-time cost tracking:

**Pricing (as of 2024)**:
- **Claude 3 Sonnet**: $3/M input tokens, $15/M output tokens
- **Claude 3 Haiku**: $0.25/M input tokens, $1.25/M output tokens

**Tips for cost optimization**:
- Use Claude 3 Haiku for standard test generation
- Reduce temperature for more consistent, shorter responses
- Lower max tokens setting to reduce output costs
- Process stories in batches to optimize API calls

## 📦 Dependencies

- **streamlit**: Web UI framework
- **pandas**: Data manipulation and export
- **boto3**: AWS SDK for Bedrock integration
- **faker**: Synthetic data generation
- **numpy**: Numerical operations

See `requirements.txt` for complete list and versions.

## 🔄 Workflow Example

```
1. Generate synthetic user stories
   └─> python3 testdatagenerator.py
   └─> Creates: insurance_user_stories.csv

2. Launch AI test case generator
   └─> streamlit run app.py

3. Configure AWS Bedrock credentials

4. Upload the generated CSV file

5. Review metrics and costs

6. Download test plan CSV

7. Integrate with your test management tool
```

## 📈 Sample Output

### User Story Example:
```
FormattedID: US00001
Name: As a Claims Adjuster, I want to perform Fraud Detection, so that I can ensure regulatory compliance.
Description: The current system lacks efficiency in handling premium during the Fraud Detection phase...
AcceptanceCriteria:
- Verify that the Claims Adjuster can access the Fraud Detection screen.
- Ensure premium is calculated correctly within 2 decimal places.
- System must return an error if input is invalid.
```

### Test Case Example:
```
TestID: TC-US00001-01
Type: Positive
Summary: Verify fraud detection system accepts valid claim
Steps: 1. Login as Claims Adjuster 2. Navigate to Fraud Detection 3. Submit valid claim
Expected_Result: System processes claim and displays confirmation
Confidence: 0.95
EstimatedCost: $0.0042
```

## 🛠️ Advanced Features

### Custom Model Configuration
Modify model parameters in the sidebar:
- **Temperature**: Control response variability
- **Max Tokens**: Limit response length for cost control
- **Region Selection**: Choose optimal AWS region

### Batch Processing
The application processes up to 5 user stories per run. To modify:
```python
# In app.py, change the limit
stories_to_process = df.head(10)  # Process 10 instead of 5
```

### Token Usage Analysis
Monitor token consumption by test case type to optimize costs based on test complexity.

## 🐛 Troubleshooting

### AWS Credentials Error
- Verify credentials are correct
- Check AWS Access Key ID format
- Ensure Bedrock service is available in your region

### No Test Cases Generated
- Check AWS credentials are saved
- Verify Bedrock access is enabled
- Review CloudWatch logs for API errors

### High Token Usage
- Reduce max tokens setting
- Lower temperature for shorter responses
- Use Claude 3 Haiku instead of Sonnet

## 📝 Contributing

Contributions are welcome! Please feel free to:
- Submit pull requests with improvements
- Open issues for bugs and feature requests
- Suggest enhancements to test generation quality

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review AWS Bedrock documentation
3. Open an issue on the repository
4. Contact your AWS support team for credential issues

## 🔗 Related Resources

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Claude Model API Documentation](https://docs.anthropic.com/bedrock/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Faker Library Documentation](https://faker.readthedocs.io/)
