# run.py

# from app.api.gmail_client import GmailClient
# from app.api.yahoo_client import YahooIMAPClient
from app.api.outlook_client import OutlookIMAPClient
from app.services.email_processing_service import EmailProcessingService
from app.repository.db import setup_database_session
from app.repository.db import save_to_database
from config.config import load_config


def main():
    # 1. Initialize configurations, services, and the database
    config = load_config()

    outlook_client = OutlookIMAPClient(config)
    email_processor = EmailProcessingService()
    db_session = setup_database_session(config)

    # 2. Fetch emails
    emails = outlook_client.fetch_emails(query="job posting")

    # 3. Process emails
    for email in emails:
        job_posting = email_processor.process_email(email)
        save_to_database(job_posting, db_session)

    # 4. Close resources
    # db_session.close()


if __name__ == "__main__":
    main()
