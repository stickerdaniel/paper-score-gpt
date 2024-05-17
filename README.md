
# PaperScoreGPT

A Python project leveraging OpenAI's GPT API to evaluate research papers and update an Excel file containing an overview of these papers. It reads key paper details such as abstract, title, publication year, and citation count, then sends a request to the OpenAI API for evaluation. The returned assessment is used to update the Excel sheet with a relevance score, reasons for the score, and additional insights. This project is ideal for academic research and provides an efficient way to automate a preliminary literature review for a large collection of papers. It helps you quickly filter out papers that are not directly relevant to your research topic.

<img width="1671" alt="Bildschirmfoto 2024-04-25 um 21 06 19" src="https://github.com/stickerdaniel/PaperScoreGPT/assets/63877413/bc7144aa-88bb-42b1-a6ab-2c808f9270cc">

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/stickerdaniel/PaperScoreGPT.git
   ```

2. Install the required dependencies:

   ```bash
   cd PaperScoreGPT
   ```
   ```bash
   pip install -r requirements.txt
   ```

## Obtaining OpenAI API Key

To use PaperScoreGPT, you will need an OpenAI API key.

1. Visit the [OpenAI website](https://www.openai.com/) and sign up for an account if you haven't already.
2. After signing up, navigate to the [API key management page](https://platform.openai.com/api-keys) and copy your API key.

## Configuration

Before running the project, you need to set up the `config.json` file in the root directory of the project. Create a `config.json` file with the following content:

```json
{
    "api_key": "YOUR_API_KEY_HERE",
    "excel_file_path": "Literature_Proseminar_Gamification_merged.xlsx",
    "sheet_name": "merged results no duplicates",
    "research_topic": "Gamification in Education",
    "research_topic_note": "Keep the focus on gamification in educational contexts.",
    "required_fields": ["Title", "Abstract"],
    "openai_model": "gpt-3.5-turbo"  // Use "gpt-3.5-turbo" for cheaper and "gpt-4" or "gpt-4-turbo" for better quality
}
```

Replace `"YOUR_API_KEY_HERE"` with your actual OpenAI API key. You can specify the OpenAI model to use (`gpt-3.5-turbo`, `gpt-4`, or `gpt-4-turbo`).

## Usage

1. Ensure you have set up the necessary API key in your `config.json`.

2. Run the main program:

   ```bash
   python review_sources.py
   ```

This will process the specified Excel file and update it with evaluations from the OpenAI API.
