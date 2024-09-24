from .config import Config
from .services.email_processor import EmailProcessor
from .email_client.pop3_client import POP3EmailClient
from .storage.notion_api import NotionClient
from .parsers.email_parsers.builtin_email_parser import BuiltInEmailParser

def main():
    config = Config()

    email_client = POP3EmailClient(config.email_client_config)
    storage_client = NotionClient(config.notion_config)

    email_parsers = [BuiltInEmailParser(config.notion_config)]  # Add more email parsers here
    web_parsers = []  # Empty for now, add web parsers in the future

    processor = EmailProcessor(
        email_client=email_client,
        storage_client=storage_client,
        email_parsers=email_parsers,
        web_parsers=web_parsers
    )

    processor.process_emails()

if __name__ == "__main__":
    main()
