from typing import List, Optional, Dict
from pydantic import BaseModel, Field, EmailStr
from pydantic_ai import Agent, RunContext, Tool
from pydantic_ai.models.openai import OpenAIModel
import httpx
from bs4 import BeautifulSoup
import os
from linkedin_api import Linkedin
import getpass
import time
from datetime import datetime, timedelta
import re
from urllib.parse import urlparse

#Defines the input model for company research requests 
class CompanyResearchRequest(BaseModel):
    """Input model for company research requests"""
    company_name: str = Field(description="Name of the company to research")
    additional_info: Optional[str] = Field(
        default=None,
        description="Any additional context or specific aspects to focus on"
    )

#Defines the output model for company research requests 
class CompanyOverview(BaseModel):
    """Structured response model for company research"""
    website: str = Field(description="Company's main website URL")
    linkedin: str = Field(description="Company's LinkedIn profile URL")
    summary: str = Field(description="Concise summary of the company")
    purpose: str = Field(description="Company's main purpose and mission")
    products: List[str] = Field(description="Key products and services")
    competitors: List[str] = Field(description="Main competitors in the market")
    funding_info: Optional[Dict] = Field(
        default=None,
        description="Funding information including round and amount"
    )
    news: Optional[List[Dict]] = Field(
        default=None,
        description="Recent news articles about the company"
    )
    videos: Optional[List[Dict]] = Field(
        default=None,
        description="Relevant videos about the company"
    )
    follow_up_questions: List[str] = Field(description="Recommended follow-up questions")
    interview_questions: List[str] = Field(description="Recommended interview questions")

#Defines the agent for researching companies and generating comprehensive overviews
class CompanyResearchAgent(Agent):
    """Agent for researching companies and generating comprehensive overviews"""
    
    def __init__(self, model: OpenAIModel):
        super().__init__(
            model=model,
            result_type=CompanyOverview,
            system_prompt=(
                "You are an expert company research analyst. Your task is to gather and analyze "
                "information about companies to create comprehensive overviews. You should:\n"
                "1. Use the provided tools to gather information from various sources\n"
                "2. Structure the information clearly and concisely\n"
                "3. Identify key aspects like products, competitors, and funding\n"
                "4. Generate relevant follow-up and interview questions\n"
                "5. Provide sources for all information\n\n"
                "Always maintain objectivity and verify information from multiple sources."
            ),
            tools=[
                Tool(self.get_website_info, takes_ctx=True),
                Tool(self.get_linkedin_info, takes_ctx=True)
            ]
        )
        self.http_client = httpx.AsyncClient()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.linkedin_username = None
        self.linkedin_password = None
        self.linkedin_api = None
        self.credentials_timestamp = None
        # Credentials expire after 30 days - adjust this value to change the expiration period
        self._CREDENTIALS_TIMEOUT = timedelta(days=30)

    def _validate_email(self, email: str) -> bool:
        """
        Validate email format.
        """
        try:
            EmailStr.validate(email)
            return True
        except ValueError:
            return False

    def _validate_password(self, password: str) -> bool:
        """
        Validate password is not empty.
        """
        return bool(password)

    def _clear_credentials(self) -> None:
        """
        Clear stored credentials and API client.
        """
        self.linkedin_username = None
        self.linkedin_password = None
        self.linkedin_api = None
        self.credentials_timestamp = None

    def _are_credentials_valid(self) -> bool:
        """
        Check if stored credentials are still valid and not expired.
        """
        if not all([self.linkedin_username, self.linkedin_password, self.credentials_timestamp]):
            return False
        
        # Check if credentials have expired
        if datetime.now() - self.credentials_timestamp > self._CREDENTIALS_TIMEOUT:
            self._clear_credentials()
            return False
        
        return True

    async def _get_linkedin_credentials(self) -> None:
        """
        Prompt for LinkedIn credentials if not already set or expired.
        """
        if not self._are_credentials_valid():
            print("\nLinkedIn credentials are required to access company information.")
            print("Your credentials will be stored securely in memory for 30 days.")
            
            while True:
                email = input("Please enter your LinkedIn email: ").strip()
                if self._validate_email(email):
                    break
                print("Invalid email format. Please try again.")
            
            while True:
                password = getpass.getpass("Please enter your LinkedIn password: ").strip()
                if self._validate_password(password):
                    break
                print("Password cannot be empty. Please try again.")
            
            try:
                # Initialize LinkedIn API client with new credentials
                self.linkedin_api = Linkedin(email, password)
                # Test the credentials with a simple API call
                self.linkedin_api.get_profile()
                
                # Store credentials only if authentication is successful
                self.linkedin_username = email
                self.linkedin_password = password
                self.credentials_timestamp = datetime.now()
                
                print("LinkedIn credentials validated successfully.")
            except Exception as e:
                print(f"Failed to authenticate with LinkedIn: {str(e)}")
                self._clear_credentials()
                raise

    async def cleanup(self) -> None:
        """
        Clean up resources and clear sensitive data.
        """
        self._clear_credentials()
        await self.http_client.aclose()

    async def research_company(self, request: CompanyResearchRequest) -> CompanyOverview:
        """
        Research a company and return a comprehensive overview.
        """
        # Create a context for the research
        context = RunContext(
            user_prompt=(
                f"Research the company: {request.company_name}\n"
                f"Additional context: {request.additional_info or 'None'}\n\n"
                "Please use the available tools to gather information and create a comprehensive overview."
            ),
            deps=request
        )
        
        # Run the research process
        response = await self.run(context)
        return response.data

    async def _is_valid_company_website(self, url: str, company_name: str) -> bool:
        """
        Validate if a URL is a valid company website.
        """
        try:
            # Check if URL is accessible
            response = await self.http_client.get(url, headers=self.headers, timeout=5.0)
            if response.status_code != 200:
                return False
            
            # Parse the URL
            parsed_url = urlparse(url)
            if not parsed_url.netloc:
                return False
            
            # Check if the domain contains the company name
            domain = parsed_url.netloc.lower()
            clean_company = re.sub(r'[^a-zA-Z0-9]', '', company_name.lower())
            
            if clean_company not in domain:
                return False
            
            # Check if the page contains company name
            soup = BeautifulSoup(response.text, 'html.parser')
            page_text = soup.get_text().lower()
            
            # Look for company name in title and meta tags
            title = soup.title.string.lower() if soup.title else ""
            meta_description = ""
            meta_desc_tag = soup.find('meta', attrs={'name': 'description'})
            if meta_desc_tag:
                meta_description = meta_desc_tag.get('content', '').lower()
            
            # Check if company name appears in key locations
            if (clean_company in title or 
                clean_company in meta_description or 
                clean_company in page_text[:1000]):  # First 1000 chars
                return True
            
            return False
            
        except Exception:
            return False

    @Tool(name="scrape_company_website")
    async def get_website_info(self, ctx: RunContext[CompanyResearchRequest]) -> Dict:
        """
        Get information from the company's website.
        """
        company_name = ctx.deps.company_name
        print(f"Gathering website information for {company_name}")
        
        try:
            # Get the website URL from the AI agent's response
            response = await self.model.generate(
                f"Please provide the official website URL for {company_name}. "
                "Only respond with the URL, nothing else."
            )
            url = response.strip()
            
            if not url or not url.startswith(('http://', 'https://')):
                return {
                    "url": "",
                    "content": "Could not find company website",
                    "status": "error",
                    "error": "Invalid website URL"
                }
            
            # Validate and scrape the website
            if await self._is_valid_company_website(url, company_name):
                content = await self._scrape_website(url)
                return {
                    "url": url,
                    "content": content,
                    "status": "success",
                    "source": "ai_agent"
                }
            
            return {
                "url": "",
                "content": "Could not validate company website",
                "status": "error",
                "error": "Website validation failed"
            }
            
        except Exception as e:
            print(f"Error gathering website info: {str(e)}")
            return {
                "url": "",
                "content": "",
                "status": "error",
                "error": str(e)
            }

    @Tool(name="fetch_linkedin_company_data")
    async def get_linkedin_info(self, ctx: RunContext[CompanyResearchRequest]) -> Dict:
        """
        Get information from the company's LinkedIn profile using the LinkedIn API.
        """
        company_name = ctx.deps.company_name
        print(f"Gathering LinkedIn information for {company_name}")
        
        try:
            # Ensure we have LinkedIn credentials
            await self._get_linkedin_credentials()
            
            # Search for the company
            company_search = self.linkedin_api.search_companies(company_name, limit=1)
            
            if not company_search:
                return {
                    "url": "",
                    "content": "Company not found on LinkedIn",
                    "status": "error",
                    "error": "Company not found"
                }
            
            # Get company details
            company_id = company_search[0]['entity_id']
            company_info = self.linkedin_api.get_company(company_id)
            
            # Extract relevant information
            content = {
                "name": company_info.get('name'),
                "description": company_info.get('description'),
                "industry": company_info.get('industry'),
                "company_size": company_info.get('staffCount'),
                "headquarters": company_info.get('headquarters'),
                #"specialties": company_info.get('specialties', []),
                #"founded": company_info.get('founded'),
                "website": company_info.get('website'),
                #"followers": company_info.get('followingInfo', {}).get('followerCount'),
                "employee_count": company_info.get('staffCount'),
                #"recent_posts": company_info.get('posts', [])[:5]  # Get 5 most recent posts
            }
            
            return {
                "url": f"https://www.linkedin.com/company/{company_id}",
                "content": content,
                "status": "success"
            }
            
        except Exception as e:
            print(f"Error gathering LinkedIn info: {str(e)}")
            return {
                "url": "",
                "content": "",
                "status": "error",
                "error": str(e)
            }

#Only used for scraping the main page of the company website.   
    async def _scrape_website(self, url: str) -> str:
        """
        Scrape content from a website.
        """
        try:
            response = await self.http_client.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text
        except Exception as e:
            print(f"Error scraping website {url}: {str(e)}")
            return "" 