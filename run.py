from app.api.pop3_client import POP3Client
from app.services.email_processing_service import EmailProcessingService
from app.repository.db import setup_database_session
from app.repository.db import save_to_database
from config.config import Config


def main():
    # 1. Initialize configurations, services, and the database
    config = Config.load_config()
    pop3_client = POP3Client(config)
    email_processor = EmailProcessingService()
    db_session = setup_database_session(config)

    # 2. Fetch emails
    emails = pop3_client.fetch_emails()

    # 3. Process emails
    for email in emails:
        job_posting = email_processor.process_email(email)
        save_to_database(job_posting, db_session)

    # 4. Close resources
    # db_session.close()


if __name__ == "__main__":
    main()
