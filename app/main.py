# app/main.py

from config import Config
from services.email_processor import EmailProcessor
from email_client.pop3_client import POP3EmailClient
from storage.notion_client import NotionClient
from parsers.email_parsers.builtin_parser import BuiltInEmailParser
from parsers.web_parsers.builtin_web_parser import BuiltInWebParser

def main():
    # Load configuration
    config = Config()

    # Initialize clients using dependency injection
    email_client = POP3EmailClient(config.email_client_config)
    storage_client = NotionClient(config.notion_config)

    # Initialize parsers
    email_parsers = [BuiltInEmailParser()]
    web_parsers = [BuiltInWebParser()]

    # Initialize the email processor
    processor = EmailProcessor(
        email_client=email_client,
        storage_client=storage_client,
        email_parsers=email_parsers,
        web_parsers=web_parsers
    )

    # Start processing emails
    processor.process_emails()

if __name__ == "__main__":
    main()
