# Company Research Agent

A web application that speeds up company research by providing quick, comprehensive company overviews and integrating with popular note-taking platforms.

## Features

- Quick company research and overview generation using AI
- Integration with Notion and Google Docs (requires API credentials)
- Company information including:
  - Website and LinkedIn links (requires LinkedIn credentials)
  - Company summary and purpose
  - Key products & features
  - Competitors
  - Funding information
  - Recent news and videos (coming soon)
- Follow-up questions and interview preparation
- Weekly email notifications for company updates (coming soon)

## Project Structure

```
research_agent_pydantic/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── services/
│   │   └── utils/
│   ├── tests/
│   └── alembic/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── utils/
│   └── public/
└── docs/
```

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```
5. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Required API Keys

The following API keys are required for full functionality:
- OpenAI API Key (required)
- LinkedIn credentials (required for company information)
- Notion API Key and Database ID (optional, for Notion integration)
- Google API credentials (optional, for Google Docs integration)

## Development

- Backend: FastAPI
- Frontend: React
- Database: PostgreSQL (planned for future use)
- Authentication: JWT (planned for future use)
- AI: OpenAI GPT-4

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT 