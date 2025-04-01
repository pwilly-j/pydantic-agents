from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic_ai.models.openai import OpenAIModel
from app.models.company_agent import CompanyResearchAgent, CompanyResearchRequest, CompanyOverview
from app.core.config import settings
from app.services.integration_service import IntegrationService
import uvicorn

app = FastAPI(
    title="Company Research Agent",
    description="API for company research and analysis using AI",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
model = OpenAIModel("gpt-4")
research_agent = CompanyResearchAgent(model)
integration_service = IntegrationService()

# Set up Notion integration if credentials are available
if settings.NOTION_API_KEY and settings.NOTION_DATABASE_ID:
    integration_service.setup_notion(
        settings.NOTION_API_KEY,
        settings.NOTION_DATABASE_ID
    )

@app.get("/")
async def root():
    return {"message": "Welcome to Company Research Agent API"}

@app.post("/research/company", response_model=CompanyOverview)
async def research_company(request: CompanyResearchRequest):
    """
    Research a company and return a comprehensive overview.
    """
    return await research_agent.research_company(request)

@app.post("/export/notion")
async def export_to_notion(company_data: CompanyOverview):
    """
    Export company research to Notion.
    """
    return await integration_service.export_to_notion(company_data.model_dump())

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 