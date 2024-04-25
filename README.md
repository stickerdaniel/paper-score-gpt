# PaperScoreGPT

A Python project leveraging OpenAI's GPT API to evaluate research papers and update an Excel file containing an overview of these papers. It reads key paper details such as abstract, title, publication year, and citation count, then sends a request to the OpenAI API for evaluation. The returned assessment is used to update the Excel sheet with a relevance score, reasons for the score, and additional insights. This project is ideal for academic research and provides an efficient way to automate a preliminary literature review for a large collection of papers. It helps you quickly filter out papers that are not directly relevant to your research topic.
<img width="1671" alt="Bildschirmfoto 2024-04-25 um 21 06 19" src="https://github.com/stickerdaniel/PaperScoreGPT/assets/63877413/bc7144aa-88bb-42b1-a6ab-2c808f9270cc">

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/stickerdaniel/GPTifyGPTify.git
   ```

3. Install the required dependencies:

   ```bash
   cd GPTify
   ```
   ```bash
   pip install -r requirements.txt
   ```

## Obtaining API Keys

To use GPTify, you will need an OpenAI API key.

### OpenAI API Key

1. Visit the [OpenAI website](https://www.openai.com/) and sign up for an account if you haven't already.
2. After signing up, navigate to the [API key management page](https://platform.openai.com/api-keys) and copy your API key.

## Usage

1. Set up the necessary API key in your environment variables.

2. Run the main program:
   ```bash
   python review_sources.py
   ```
