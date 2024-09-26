import logging

logger = logging.getLogger(__name__)

class EmailProcessor:
    def __init__(self, email_client, storage_client, email_parsers, web_parsers):
        self.email_client = email_client
        self.storage_client = storage_client
        self.email_parsers = email_parsers
        self.web_parsers = web_parsers

    def process_emails(self):
        emails = self.email_client.fetch_emails()

        for index, email in enumerate(emails, start=1):
            logger.info("Processing email (%s): %s", email.get('Date'), email.get('Subject'))
            parser = self._select_email_parser(email)

            if not parser:
                logger.warning("No parser found for email (%s): %s", email.get('Date'), email.get('Subject'))
                continue

            logger.info("Using parser: %s", parser.__class__.__name__)
            jobs = parser.parse(email)

            for job in jobs:
                if not self.storage_client.job_exists(job):
                    self.storage_client.insert_job(job)

            # Optionally scrape additional details from web pages
            # web_parser = self._select_web_parser(job.url)
            # if web_parser:
            #     additional_details = web_parser.parse(job.url)
            #     job.update_details(additional_details)

            if len(jobs) > 0:
                logger.info(f"Found {len(jobs)} job(s), archiving email({index}): {email.get('Message-ID')}")

                # Use the save_email method, which now returns a boolean indicating success
                save_success = self.email_client.save_email(email)

                if save_success:
                    logger.info(f"Email ({index}) saved successfully, proceeding to delete from server.")
                    self.email_client.delete_email(index)
                else:
                    logger.error(f"Failed to save email ({index}), skipping deletion.")

        self.email_client.logout()

    def _select_email_parser(self, email):
        for parser in self.email_parsers:
            if parser.can_parse(email):
                return parser
        return None

    def _select_web_parser(self, url):
        for parser in self.web_parsers:
            if parser.can_parse(url):
                return parser
        return None
