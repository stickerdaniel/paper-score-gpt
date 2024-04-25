import re
import pandas as pd
import os
import json
from openai import OpenAI, OpenAIError  # Updated import

# Set the OpenAI API key using environment variables for security
api_key = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY_HERE")

# Instantiate the OpenAI client
client = OpenAI(api_key=api_key)

# File path to the Excel file
excel_file_path = 'Literature_Proseminar_Gamification_merged_r2review.xlsx'
# Default sheet name (user-specified)
sheet_name = 'merged results no duplicates'

# Append '_reviewed' to the file name for the reviewed data
excel_file_path_reviewed = excel_file_path.replace('.xlsx', '_reviewed.xlsx')

# Load the data from the specified Excel sheet with error handling
if not os.path.exists(excel_file_path):
    raise FileNotFoundError(f"The file {excel_file_path} does not exist.")

try:
    # Read data and trim column names to avoid extra spaces
    data = pd.read_excel(excel_file_path, sheet_name=sheet_name)
    data.columns = data.columns.str.strip()  # Trim leading/trailing spaces from column names
except Exception as e:
    raise ValueError(f"Error reading sheet '{sheet_name}' from the Excel file: {e}")

# Ensure consistent initialization of new columns
new_columns = ['Relevance Score', 'Reason', 'Notes', 'Added Value']
for col_name in new_columns:
    if col_name not in data.columns:
        data[col_name] = 'not processed yet'  # Initialize with a default value

# Define required fields for processing
required_fields = ['Title', 'Abstract']


# Helper function to build a JSON object for ChatGPT evaluation
def build_paper_json(row, fields):
    paper_json = {}
    for field in fields:
        if field in data.columns:
            # Convert to string, trim, and ensure it's not empty
            value = str(row[field]).strip()
            paper_json[field] = value if value else 'N/A'
        else:
            paper_json[field] = 'N/A'  # Field does not exist in the data
    return paper_json


# Function to evaluate the paper with ChatGPT using the new API client
def evaluate_paper_with_chatgpt(paper_json):
    prompt = f"""
    I am working on a research project on "Gamification in Education". Please evaluate the following paper critically and provide in a short answer:
    - The added value of this paper to my research. (if any) (1-2 sentences)
    - Any additional notes or observations regarding the paper in bullet points. (1-3 short points)
    - A score (0-100%) indicating the relevance of this paper to my research project. (x%)
    - A reason explaining why the score was given. (1-2 sentences)

    Here is the information of the paper to be evaluated:
    Title: {paper_json['Title']}
    Abstract: {paper_json['Abstract']}
    Authors: {paper_json.get('Authors', 'N/A')}
    Publication Year: {paper_json.get('Publication Year', 'N/A')}
    Times Cited: {paper_json.get('Times Cited, All Databases', 'N/A')}

    Note: The focus is on gamification in educational contexts. Articles related to medical applications or other irrelevant fields should be scored accordingly. Be critical and provide constructive feedback. If the paper is not relevant (<50% score), please provide a briefer answer with really short sentences.

    Here is an example of the JSON format I expect for the response:
    {{"score": "80%", "reason": "The paper provides a comprehensive overview of gamification in educational settings.", "notes": "- Seems like there are no recent examples of gamification in practice.", "added value": "The paper offers a unique perspective on the impact of gamification on student engagement."}}
    """

    try:
        # Make the API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )
        # Extract the response content
        response_content = response.choices[0].message.content

        # Split at double quotes to isolate quoted content from non-quoted sections
        parts = response_content.split('"')  # Split into non-quoted and quoted parts

        # Clean non-quoted sections to remove control characters, excess spaces, and newlines
        for i in range(len(parts)):
            if i % 2 == 0:  # Non-quoted sections
                # Remove all control characters and extra spaces
                parts[i] = re.sub(r'[\x00-\x1F\x7F]+', '', parts[i])  # Remove control characters
                parts[i] = parts[i].strip()

        # Reconstruct the JSON structure by joining the parts with double quotes
        cleaned_json_str = '"'.join(parts)  # Rejoin parts with double quotes

        # Debugging: print raw and sanitized content
        print(f"Review for paper '{paper_json['Title']}':")
        print("Raw content:", response_content)  # Raw content for debugging
        print("Cleaned JSON:", cleaned_json_str)  # Cleaned JSON for debugging

        # Attempt to parse the sanitized content into JSON
        try:
            evaluation = json.loads(cleaned_json_str)  # Convert from JSON string to dictionary
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            evaluation = {
                "score": "-",
                "reason": "JSON parsing error",
                "notes": "An error occurred while parsing the OpenAI response.",
                "added value": "-",
            }
            # try again
            return evaluate_paper_with_chatgpt(paper_json)

    except OpenAIError as e:
        print(f"Error during OpenAI API call: {e}")
        evaluation = {
            "score": "-",
            "reason": "API error",
            "notes": "An error occurred during the API call.",
            "added value": "-",
        }

    return evaluation


# Iterate over each row in the Excel file and evaluate the paper
for index, row in data.iterrows():
    # Check if required fields exist and are not empty
    if not all(field in data.columns and pd.notna(row[field]) for field in required_fields):
        print(f"Skipping row {index} due to missing required fields.")
        continue

    # Build a JSON object with the paper row information
    paper_json = build_paper_json(row, data.columns)

    print(f"\n\nReviewing paper {index + 1}:")
    print(paper_json)  # Print the JSON object for debugging

    # Evaluate the paper with ChatGPT
    evaluation = evaluate_paper_with_chatgpt(paper_json)

    # Update the Excel file with the evaluation results
    data.at[index, 'Relevance Score'] = evaluation.get("score", 'N/A')
    data.at[index, 'Reason'] = evaluation.get("reason", 'N/A')
    data.at[index, 'Notes'] = evaluation.get("notes", 'N/A')
    data.at[index, 'Added Value'] = evaluation.get("added value", 'N/A')

    # Save the updated Excel file with error handling
    try:
        data.to_excel(excel_file_path_reviewed, index=False)
        print(f"Review completed. Results saved to {excel_file_path_reviewed}")
    except Exception as e:
        print(f"Failed to save the updated Excel file: {e}")

    # Option to abort the script but still save the data
    x = 'y'
    # x = input("Continue and review? (y/n): ") # Uncomment this line to wait for user input after each review
    if x.lower() != 'y':
        break
