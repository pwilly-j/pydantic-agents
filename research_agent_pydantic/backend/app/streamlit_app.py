import streamlit as st
import asyncio
from app.models.company_agent import CompanyResearchAgent, CompanyResearchRequest
from pydantic_ai.models.openai import OpenAIModel
from app.core.config import settings

# Initialize the research agent
model = OpenAIModel("gpt-4")
research_agent = CompanyResearchAgent(model)

# Set page config
st.set_page_config(
    page_title="Company Research Agent",
    page_icon="🔍",
    layout="wide"
)

# Add custom CSS
st.markdown("""
    <style>
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
    }
    .stTextArea > div > div > textarea {
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("🔍 Company Research Agent")
st.markdown("""
    This tool helps you gather comprehensive information about companies using AI.
    Enter a company name and any additional context to get started.
    """)

# Create two columns for input
col1, col2 = st.columns([2, 1])

with col1:
    company_name = st.text_input(
        "Company Name",
        placeholder="Enter the company name (e.g., Apple, Microsoft, Google)",
        key="company_name"
    )

with col2:
    additional_info = st.text_area(
        "Additional Context (Optional)",
        placeholder="Any specific aspects you'd like to focus on?",
        height=100,
        key="additional_info"
    )

# Research button
if st.button("Research Company", type="primary"):
    if not company_name:
        st.error("Please enter a company name")
    else:
        with st.spinner("Researching company..."):
            try:
                # Create research request
                request = CompanyResearchRequest(
                    company_name=company_name,
                    additional_info=additional_info if additional_info else None
                )
                
                # Run research
                result = asyncio.run(research_agent.research_company(request))
                
                # Display results in tabs
                tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Products & Competitors", "Funding & News", "Interview Questions"])
                
                with tab1:
                    st.subheader("Company Overview")
                    st.write("**Website:**", result.website)
                    st.write("**LinkedIn:**", result.linkedin)
                    st.write("**Summary:**", result.summary)
                    st.write("**Purpose:**", result.purpose)
                
                with tab2:
                    st.subheader("Products & Services")
                    for product in result.products:
                        st.write(f"• {product}")
                    
                    st.subheader("Main Competitors")
                    for competitor in result.competitors:
                        st.write(f"• {competitor}")
                
                with tab3:
                    if result.funding_info:
                        st.subheader("Funding Information")
                        st.write(result.funding_info)
                    
                    if result.news:
                        st.subheader("Recent News")
                        for news_item in result.news:
                            st.write(f"• {news_item}")
                    
                    if result.videos:
                        st.subheader("Relevant Videos")
                        for video in result.videos:
                            st.write(f"• {video}")
                
                with tab4:
                    st.subheader("Follow-up Questions")
                    for question in result.follow_up_questions:
                        st.write(f"• {question}")
                    
                    st.subheader("Interview Questions")
                    for question in result.interview_questions:
                        st.write(f"• {question}")
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Add footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Built with ❤️ using Streamlit and Pydantic</p>
    </div>
    """, unsafe_allow_html=True) 