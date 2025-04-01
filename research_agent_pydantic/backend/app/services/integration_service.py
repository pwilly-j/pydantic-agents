from typing import Dict, Optional
from notion_client import Client as NotionClient
# from google.oauth2.credentials import Credentials
# from googleapiclient.discovery import build
# from google.oauth2 import service_account
from pydantic import BaseModel

class IntegrationService:
    def __init__(self):
        self.notion_client = None
        # self.google_docs_service = None

    def setup_notion(self, notion_token: str, database_id: str):
        """
        Set up Notion integration with API token and database ID.
        """
        self.notion_client = NotionClient(auth=notion_token)
        self.notion_database_id = database_id

    # def setup_google_docs(self, credentials_json: str):
    #     """
    #     Set up Google Docs integration with service account credentials.
    #     """
    #     credentials = service_account.Credentials.from_service_account_info(
    #         credentials_json,
    #         scopes=['https://www.googleapis.com/auth/drive.file']
    #     )
    #     self.google_docs_service = build('docs', 'v1', credentials=credentials)

    async def export_to_notion(self, company_data: Dict) -> Dict:
        """
        Export company research to Notion database.
        """
        if not self.notion_client:
            raise ValueError("Notion integration not set up")

        # Format the data for Notion
        notion_data = {
            "parent": {"database_id": self.notion_database_id},
            "properties": {
                "Company Name": {"title": [{"text": {"content": company_data.get("name", "")}}]},
                "Website": {"url": company_data.get("website", "")},
                "LinkedIn": {"url": company_data.get("linkedin", "")},
                "Summary": {"rich_text": [{"text": {"content": company_data.get("summary", "")}}]},
                "Purpose": {"rich_text": [{"text": {"content": company_data.get("purpose", "")}}]},
                "Products": {"multi_select": [{"name": product} for product in company_data.get("products", [])]},
                "Competitors": {"multi_select": [{"name": competitor} for competitor in company_data.get("competitors", [])]},
                "Funding Round": {"select": {"name": company_data.get("funding_info", {}).get("round", "")}},
                "Funding Amount": {"rich_text": [{"text": {"content": company_data.get("funding_info", {}).get("amount", "")}}]}
            }
        }

        # Create the page in Notion
        response = self.notion_client.pages.create(**notion_data)
        
        # TODO: Implement news and video integration once those features are available
        # if company_data.get("news"):
        #     await self._add_news_to_notion(response["id"], company_data["news"])
        
        # if company_data.get("videos"):
        #     await self._add_videos_to_notion(response["id"], company_data["videos"])

        return {"notion_page_id": response["id"]}

    # TODO: Implement news and video integration once those features are available
    # async def _add_news_to_notion(self, parent_page_id: str, news_items: list):
    #     """
    #     Add news items as child pages in Notion.
    #     """
    #     for news in news_items:
    #         news_data = {
    #             "parent": {"page_id": parent_page_id},
    #             "properties": {
    #                 "Title": {"title": [{"text": {"content": news.get("title", "")}}]},
    #                 "URL": {"url": news.get("url", "")}
    #             }
    #         }
    #         self.notion_client.pages.create(**news_data)

    # async def _add_videos_to_notion(self, parent_page_id: str, video_items: list):
    #     """
    #     Add video items as child pages in Notion.
    #     """
    #     for video in video_items:
    #         video_data = {
    #             "parent": {"page_id": parent_page_id},
    #             "properties": {
    #                 "Title": {"title": [{"text": {"content": video.get("title", "")}}]},
    #                 "URL": {"url": video.get("url", "")}
    #             }
    #         }
    #         self.notion_client.pages.create(**video_data)

    # async def export_to_google_docs(self, company_data: Dict) -> Dict:
    #     """
    #     Export company research to Google Docs.
    #     """
    #     if not self.google_docs_service:
    #         raise ValueError("Google Docs integration not set up")
    #
    #     # Create a new document
    #     document = {
    #         'title': f"Company Research: {company_data.get('name', '')}"
    #     }
    #     doc = self.google_docs_service.documents().create(body=document).execute()
    #     doc_id = doc.get('documentId')
    #
    #     # Format the content
    #     content = [
    #         {
    #             'insertText': {
    #                 'location': {
    #                     'index': 1
    #                 },
    #                 'text': f"Company Research: {company_data.get('name', '')}\n\n"
    #             }
    #         },
    #         {
    #             'insertText': {
    #                 'location': {
    #                     'index': 2
    #                 },
    #                 'text': f"Website: {company_data.get('website', '')}\n"
    #             }
    #         },
    #         {
    #             'insertText': {
    #                 'location': {
    #                     'index': 3
    #                 },
    #                 'text': f"LinkedIn: {company_data.get('linkedin', '')}\n\n"
    #             }
    #         },
    #         {
    #             'insertText': {
    #                 'location': {
    #                     'index': 4
    #                 },
    #                 'text': f"Summary:\n{company_data.get('summary', '')}\n\n"
    #             }
    #         },
    #         {
    #             'insertText': {
    #                 'location': {
    #                     'index': 5
    #                 },
    #                 'text': f"Purpose:\n{company_data.get('purpose', '')}\n\n"
    #             }
    #         },
    #         {
    #             'insertText': {
    #                 'location': {
    #                     'index': 6
    #                 },
    #                 'text': f"Products:\n{', '.join(company_data.get('products', []))}\n\n"
    #             }
    #         },
    #         {
    #             'insertText': {
    #                 'location': {
    #                     'index': 7
    #                 },
    #                 'text': f"Competitors:\n{', '.join(company_data.get('competitors', []))}\n\n"
    #             }
    #         }
    #     ]
    #
    #     # Add funding information if available
    #     if company_data.get("funding_info"):
    #         content.append({
    #             'insertText': {
    #                 'location': {
    #                     'index': 8
    #                 },
    #                 'text': f"Funding:\nRound: {company_data['funding_info'].get('round', '')}\n"
    #                        f"Amount: {company_data['funding_info'].get('amount', '')}\n\n"
    #             }
    #         })
    #
    #     # TODO: Implement news and video sections once those features are available
    #     # # Add news section
    #     # if company_data.get("news"):
    #     #     content.append({
    #     #         'insertText': {
    #     #             'location': {
    #     #                 'index': 9
    #     #             },
    #     #             'text': "Recent News:\n"
    #     #         }
    #     #     })
    #     #     for news in company_data["news"]:
    #     #         content.append({
    #     #             'insertText': {
    #     #                 'location': {
    #     #                     'index': 10
    #     #                 },
    #     #                 'text': f"- {news.get('title', '')}: {news.get('url', '')}\n"
    #     #             }
    #     #         })
    #
    #     # # Add videos section
    #     # if company_data.get("videos"):
    #     #     content.append({
    #     #         'insertText': {
    #     #             'location': {
    #     #                 'index': 11
    #     #             },
    #     #             'text': "\nVideos:\n"
    #     #         }
    #     #     })
    #     #     for video in company_data["videos"]:
    #     #         content.append({
    #     #             'insertText': {
    #     #                 'location': {
    #     #                     'index': 12
    #     #                 },
    #     #                 'text': f"- {video.get('title', '')}: {video.get('url', '')}\n"
    #     #             }
    #     #         })
    #
    #     # Update the document with content
    #     self.google_docs_service.documents().batchUpdate(
    #         documentId=doc_id,
    #         body={'requests': content}
    #     ).execute()
    #
    #     return {"google_doc_id": doc_id} 