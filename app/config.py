import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for loading environment variables."""

    def __init__(self):
        # Email client configuration (pop3 settings)
        self.email_client_config = {
            'server': os.getenv('POP_SERVER'),
            'port': os.getenv('POP_PORT'),
            'username': os.getenv('POP_USERNAME'),
            'password': os.getenv('POP_PASSWORD')
        }

        # Notion configuration (notion settings)
        self.notion_config = {
            'token': os.getenv('NOTION_TOKEN'),
            'database_id': os.getenv('NOTION_DATABASE_ID')
        }

        # Below is hardcoded now in main.py  ...will need an enum somewhere, at some point
        # Add email_type for easier management of email parsers
        # self.email_type = 'builtIn_jobs'

        # Validation for mandatory fields
        self._validate_config()

    def _validate_config(self):
        """Validate that all required configuration variables are set."""
        if not self.email_client_config['server']:
            raise EnvironmentError("POP_SERVER environment variable is not set.")

        if not self.email_client_config['port'].isdigit():
            raise EnvironmentError("POP_PORT environment variable is invalid. It should be an integer.")

        if not self.email_client_config['username']:
            raise EnvironmentError("POP_USERNAME environment variable is not set.")

        if not self.email_client_config['password']:
            raise EnvironmentError("POP_PASSWORD environment variable is not set.")

        if not self.notion_config['token']:
            raise EnvironmentError("NOTION_TOKEN environment variable is not set.")

        if not self.notion_config['database_id']:
            raise EnvironmentError("NOTION_DATABASE_ID environment variable is not set.")

        # Convert port to an integer
        self.email_client_config['port'] = int(self.email_client_config['port'])
