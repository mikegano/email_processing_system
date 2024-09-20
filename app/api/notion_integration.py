import os
from notion_client import Client

class NotionJobInserter:
    def __init__(self):
        # Load the Notion token from environment variables
        self.notion_token = os.getenv("NOTION_TOKEN", "")
        self.database_id = os.getenv("NOTION_DATABASE_ID", "")  # Store your database ID here
        self.notion = Client(auth=self.notion_token)

    def insert_job(self, job):
        """Inserts a single job record into the Notion database."""
        new_page = {
            "Title": {
                "title": [
                    {
                        "text": {
                            "content": job['title'],
                            "link": {"url": job['url']}  # Make title a hyperlink to the job URL
                        }
                    }
                ]
            },
            "Company": {"rich_text": [{"text": {"content": job['company']}}]},
            "Location": {"rich_text": [{"text": {"content": job['location']}}]},
            # Add Workplace select field
            "Workplace": {
                "select": {
                    "name": job['workplace']  # The workplace value should be 'Remote', 'Hybrid', or 'In Office'
                }
            }
        }

        try:
            self.notion.pages.create(parent={"database_id": self.database_id}, properties=new_page)
            print(f"Job '{job['title']}' added to the Notion database.")
        except Exception as e:
            print(f"Error inserting job into Notion: {e}")
