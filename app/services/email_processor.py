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

        for email in emails:
            logger.info("Processing email (%s): %s", email.get('Date'), email.get('Subject'))
            parser = self._select_email_parser(email)

            if not parser:
                logger.warning("No parser found for email (%s): %s", email.get('Date'), email.get('Subject'))
                continue

            logger.info("Using parser: %s", parser.__class__.__name__)
            jobs = parser.parse(email)

            for job in jobs:
                self._save_raw_html(job)

                if not self.storage_client.job_exists(job):
                    self.storage_client.insert_job(job)

            # Optionally scrape additional details from web pages
            # web_parser = self._select_web_parser(job.url)
            # if web_parser:
            #     additional_details = web_parser.parse(job.url)
            #     job.update_details(additional_details)

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

    def _save_raw_html(self, job):
        # Implement logic to save raw HTML snippets
        pass
