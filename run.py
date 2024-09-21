from app.email_client.pop3_client import POP3Client
# from app.services.email_processing_service import EmailProcessingService
# from app.repository.db import setup_database_session
# from app.repository.db import save_to_database
from app.config import Config


def main():
    # 1. Initialize configurations, services, and the database
    config = Config.load_config()
    pop3_client = POP3Client(config, email_type='builtin_jobs')
    # email_processor = EmailProcessingService()
    # db_session = setup_database_session(config)

    # 2. Fetch emails
    emails = pop3_client.fetch_emails()

    # pop3_client.display_jobs(emails)

    """
    # 3. Process emails
    for email in emails:
        job_posting = email_processor.process_email(email)
        save_to_database(job_posting, db_session)
    """
    # consider storing and deleting emails after processing
    # also will need to use URL to get job details

    # 4. Close resources
    # db_session.close()


if __name__ == "__main__":
    main()
