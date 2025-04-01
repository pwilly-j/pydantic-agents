# Company Research Agent

A powerful AI-powered tool for researching companies and generating comprehensive overviews using Streamlit and Pydantic.

## Features

- Company research and analysis
- LinkedIn integration for company data
- Website scraping and analysis
- Comprehensive company overviews including:
  - Basic information
  - Products and services
  - Competitors
  - Funding information
  - Recent news
  - Interview questions

## Prerequisites

- Python 3.8 or higher
- LinkedIn account (for accessing company data)
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd research_agent_pydantic
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your API keys:
```env
OPENAI_API_KEY=your_openai_api_key
```

## Running the Application

1. Start the Streamlit app:
```bash
streamlit run backend/app/streamlit_app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Enter a company name and any additional context you'd like to focus on

4. Click "Research Company" to start the analysis

## Usage

1. Enter the company name in the main input field
2. Optionally add any specific aspects you'd like to focus on
3. Click the "Research Company" button
4. View the results in the organized tabs:
   - Overview: Basic company information
   - Products & Competitors: Company offerings and market position
   - Funding & News: Financial information and recent updates
   - Interview Questions: Suggested questions for further research

## Note

When using the LinkedIn integration, you'll be prompted to enter your LinkedIn credentials. These credentials are stored securely in memory and will expire after 30 days.

## License

MIT License 