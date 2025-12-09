import pandas as pd
import random
import logging
from pathlib import Path
from typing import List, Dict
from faker import Faker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Faker
fake = Faker()

def generate_insurance_user_stories(num_records: int = 500) -> pd.DataFrame:
    """
    Generates synthetic user story data for an insurance application.
    
    Parameters:
        num_records (int): The number of user stories to generate. Default: 500
    
    Returns:
        pd.DataFrame: A dataframe containing the generated user stories with columns:
            - FormattedID: Unique identifier
            - Name: User story title
            - Description: Detailed description
            - Notes: Developer notes
            - AcceptanceCriteria: Acceptance criteria
    
    Raises:
        ValueError: If num_records is less than 1
    """
    if num_records < 1:
        raise ValueError("num_records must be at least 1")
    
    logger.info(f"Generating {num_records} insurance user stories...")
    
    # Domain specific lists to ensure data relevance
    roles = [
        "Policyholder", "Claims Adjuster", "Underwriter", "Insurance Agent", 
        "System Admin", "Compliance Officer", "Billing Specialist"
    ]
    
    features = [
        "First Notice of Loss (FNOL)", "Policy Renewal", "Premium Calculation", 
        "Fraud Detection", "Document Upload", "Quote Generation", 
        "Claim Status Tracking", "Deductible Adjustment", "Customer Onboarding"
    ]
    
    benefits = [
        "reduce processing time", "improve customer satisfaction", "ensure regulatory compliance",
        "minimize data entry errors", "speed up claim settlement", "increase underwriting accuracy",
        "allow for 24/7 access", "secure sensitive personal data"
    ]
    
    insurance_terms = [
        "liability coverage", "deductible", "premium", "policy limit", "subrogation",
        "indemnity", "beneficiary", "claimant", "actuarial table", "endorsement"
    ]

    data: List[Dict] = []

    for i in range(1, num_records + 1):
        # 1. FormattedID
        formatted_id = f"US{i:05d}"
        
        # Select random elements
        role = random.choice(roles)
        feature = random.choice(features)
        benefit = random.choice(benefits)
        term = random.choice(insurance_terms)
        
        # 2. Name (The Title of the User Story)
        # Structure: As a <role>, I want <feature/action>, so that <benefit>.
        name = f"As a {role}, I want to perform {feature}, so that I can {benefit}."
        
        # 3. Description
        # Generate a paragraph that mimics a business requirement description
        context_sentence = f"The current system lacks efficiency in handling {term} during the {feature} phase."
        detail_sentence = fake.sentence(nb_words=10)
        tech_note = f"The implementation should consider the impact on {random.choice(roles)} workflows."
        description = f"{context_sentence} {detail_sentence} {tech_note}"
        
        # 4. Notes
        # Random developer notes, edge cases, or priority flags
        notes_options = [
            "Requires API integration with legacy mainframe.",
            "Pending approval from Legal department.",
            f"Watch out for edge cases regarding {term}.",
            "UI mockup available in Figma.",
            "High priority due to upcoming audit.",
            "Database schema update required."
        ]
        notes = random.choice(notes_options) if random.random() > 0.3 else ""  # 30% chance of empty notes
        
        # 5. Acceptance Criteria
        # Generate bullet points
        ac_count = random.randint(3, 5)
        criteria_list = [
            f"Verify that the {role} can access the {feature} screen.",
            f"Ensure {term} is calculated correctly within 2 decimal places.",
            f"System must return an error if input is invalid.",
            f"Response time should be under 200ms."
        ]
        
        # Randomly sample unique criteria to form the block
        selected_criteria = random.sample(criteria_list, min(ac_count, len(criteria_list)))
        acceptance_criteria = "\n".join([f"- {item}" for item in selected_criteria])

        data.append({
            "FormattedID": formatted_id,
            "Name": name,
            "Description": description,
            "Notes": notes,
            "AcceptanceCriteria": acceptance_criteria
        })

    logger.info(f"Successfully generated {num_records} user stories")
    return pd.DataFrame(data)


def save_user_stories(df: pd.DataFrame, output_path: str) -> None:
    """
    Save user stories DataFrame to a CSV file.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing user stories
        output_path (str): Path where the CSV file will be saved
    
    Raises:
        IOError: If the file cannot be written
    """
    try:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        logger.info(f"Successfully saved {len(df)} records to '{output_path}'")
    except IOError as e:
        logger.error(f"Failed to save file: {e}")
        raise

if __name__ == "__main__":
    try:
        # Generate 500 sample user stories
        logger.info("Starting data generation...")
        df_user_stories = generate_insurance_user_stories(num_records=500)

        # Display the first few rows to verify
        print("\n" + "="*80)
        print("Sample Data Preview (First 5 Records):")
        print("="*80)
        print(df_user_stories.head().to_string())

        # Save to CSV for use in your ML project
        output_file = "../testcasegenerator/output/insurance_user_stories.csv"
        save_user_stories(df_user_stories, output_file)
        
        print("\n" + "="*80)
        print(f"Generation Complete! Total records: {len(df_user_stories)}")
        print("="*80 + "\n")
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise
