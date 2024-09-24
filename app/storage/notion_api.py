from notion_client import Client
from ..models.job import Job

class NotionClient:
    def __init__(self, notion_config):
        # Use the configuration passed into the class
        self.notion_token = notion_config['token']
        self.database_id = notion_config['database_id']
        self.notion = Client(auth=self.notion_token)

    def insert_job(self, job: Job):
        """Inserts a single job record into the Notion database."""
        new_page = {
            "Title": {
                "title": [
                    {
                        "text": {
                            "content": job.title,
                            "link": {"url": job.url}  # Make title a hyperlink to the job URL
                        }
                    }
                ]
            },
            "Company": {"rich_text": [{"text": {"content": job.company}}]},
            "Location": {"rich_text": [{"text": {"content": job.location}}]},
            "Workplace": {
                "select": {
                    "name": job.workplace  # 'Remote', 'Hybrid', or 'In Office'
                }
            },
            "Job URL": {
                "url": job.url
            }
        }

        try:
            self.notion.pages.create(
                parent={"database_id": self.database_id}, properties=new_page
            )
            print(f"Job '{job.title}' added to the Notion database.")
        except Exception as e:
            print(f"Error inserting job into Notion: {e}")

    def job_exists(self, job: Job):
        """Checks if a job already exists in the Notion database."""

        query = {
            "filter": {
                "property": "Job URL",  # Must match the property name in Notion
                "url": {
                    "equals": job.url
                }
            }
        }

        try:
            response = self.notion.databases.query(
                database_id=self.database_id, **query  # Unpack the query dictionary
            )
            print(f"Checking for dups. Found {len(response['results'])} results.")
            return len(response['results']) > 0
        except Exception as e:
            print(f"Error checking if job exists in Notion: {e}")
            return False
