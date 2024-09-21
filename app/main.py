from config import Config
from app.services.email_processor import EmailProcessor
from app.email_client.pop3_client import POP3EmailClient
from app.storage.notion_api import NotionClient
from app.parsers.email_parsers.builtin_email_parser import BuiltInEmailParser
from app.parsers.web_parsers.builtin_web_parser import BuiltInWebParser

def main():
    # Load configuration
    config = Config()

    # Initialize clients using dependency injection
    email_client = POP3EmailClient(config.email_client_config, config.email_type)
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
