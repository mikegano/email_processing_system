import logging

from bs4 import BeautifulSoup
from email.utils import parseaddr

from ...storage.notion_api import NotionClient
from ...parsers.base_parser import BaseParser
from ...models.job import Job

logger = logging.getLogger(__name__)

class BuiltInEmailParser(BaseParser):
    def __init__(self, notion_config):
        try:
            self.notion_inserter = NotionClient(notion_config)
        except Exception as e:
            logger.error("Failed to initialize NotionClient: %s", e)
            raise

    def can_parse(self, email):
        """Determine if this parser can handle the given email."""
        """TODO: handle forwarded emails"""

        from_address = email.get('From', '')
        subject = email.get('Subject', '')

        # Parse the email address from the 'From' header
        name, addr = parseaddr(from_address)

        # Check if the email is from 'support@builtin.com'
        if addr.lower() != 'support@builtin.com':
            logger.info("Skipping email from %s", addr)
            return False

        # Check if the subject contains "You Have New Tech Job Matches"
        if 'you have new tech job matches' not in subject.lower():
            logger.info("Skipping email with subject: %s", subject)
            return False

        return True

    def _parse_html_body(self, html_body):
        """Parse the HTML body for job information."""
        soup = BeautifulSoup(html_body, 'html.parser')

        # Find the <tr> element with id="job1"
        job_table_row = soup.find('tr', id='job1')
        if not job_table_row:
            logger.warning("No job table found in email.")
            return []

        # Find the inner table containing job postings
        inner_table = job_table_row.find('table')
        if not inner_table:
            logger.warning("No inner job table found in email.")
            return []

        # Now find all <tr> elements within the inner table
        job_elements = inner_table.find_all('td', style=lambda x: x and 'font-family:Verdana' in x)
        logger.debug(f"Found {len(job_elements)} job rows.")

        if not job_elements:
            logger.warning("No job elements found in email.")
            return []

        jobs = []
        for idx, job_element in enumerate(job_elements, start=1):
            logger.debug(f"Processing job element {idx}: {job_element}")
            job_info = self._get_job_info(job_element)
            if job_info:
                jobs.append(job_info)
            else:
                logger.warning(f"Failed to extract job info from element {idx}.")

        return jobs

    def _get_job_info(self, job_element):
        """Extract job information from a job element."""
        a_tag = job_element.find('a', href=True)
        logger.debug(f"Extracted a_tag: {a_tag}")

        if not a_tag:
            logger.warning("Failed to extract job URL from element.")
            return None
        job_url = a_tag['href']
        logger.debug(f"Job URL: {job_url}")

        title_element = job_element.find('div', style=lambda x: x and 'font-size:20px' in x)
        logger.debug(f"Title element: {title_element}")
        company_element = job_element.find('div', style=lambda x: x and 'font-size:16px' in x)
        logger.debug(f"Company element: {company_element}")

        # Find the parent div that contains the location info
        container_match = 'margin-bottom:4px;font-size:12px'
        location_container = job_element.find('div', style=lambda x: x and container_match in x)
        logger.debug(f"Location container: {location_container}")

        if not title_element or not company_element or not location_container:
            logger.warning("Failed to extract job information from element.")
            return None

        title = title_element.get_text(strip=True)
        company = company_element.get_text(strip=True)
        logger.debug(f"Extracted title: {title}, company: {company}")

        # Extract the location information from all relevant spans
        spans_match = 'vertical-align:middle'
        location_spans = location_container.find_all('span', style=lambda x: x and spans_match in x)
        logger.debug(f"Location spans: {location_spans}")

        workplace = ''
        location = ''

        # Assign values based on the number of spans found
        if len(location_spans) >= 1:
            workplace = location_spans[0].get_text(strip=True)
            logger.debug(f"Extracted workplace: {workplace}")
        if len(location_spans) >= 2:
            location = location_spans[1].get_text(strip=True)
            logger.debug(f"Extracted location: {location}")

        return Job(
            title=title,
            company=company,
            location=location,
            url=job_url,
            workplace=workplace
        )
