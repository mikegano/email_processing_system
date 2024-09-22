from bs4 import BeautifulSoup
from app.storage.notion_api import NotionClient
from app.parsers.base_parser import BaseParser

class BuiltInEmailParser(BaseParser):
    def __init__(self, notion_config):
        self.notion_inserter = NotionClient(notion_config)

    def parse(self, parsed_email):
        if not parsed_email.is_multipart():
            return {}

        for part in parsed_email.walk():
            if self._is_html_part(part):
                html_body = self._get_html_body(part)
                return self._parse_html_body(html_body)
        return {}

    def can_parse(self, email):
        # Logic to determine if this parser can handle the given email.
        # For example, you might check the subject line or sender.
        # return "builtin_jobs" in email['subject'].lower()
        return True

    def _is_html_part(self, part):
        return part.get_content_type() == "text/html"

    def _get_html_body(self, part):
        return part.get_payload(decode=True).decode()

    def _parse_html_body(self, html_body):
        soup = BeautifulSoup(html_body, 'html.parser')
        job_elements = soup.find_all('td', style=lambda x: x and 'font-family:Verdana' in x)

        if not job_elements:
            return []

        jobs = []

        for job_element in job_elements:
            job_info = self._get_job_info(job_element)
            if job_info:
                jobs.append(job_info)
                self.notion_inserter.insert_job(job_info)  # Insert job into Notion

        return jobs

    def _get_job_info(self, job_element):

        # Get the job URL
        a_tag = job_element.find('a', href=True)
        if not a_tag:
            return None
        job_url = a_tag['href']

        # Get the job title and company
        title_element = job_element.find('div', style=lambda x: x and 'font-size:20px' in x)
        company_element = job_element.find('div', style=lambda x: x and 'font-size:16px' in x)

        # Find the parent div that contains the location info
        location_container = job_element.find('div', style=lambda x: x and 'margin-bottom:4px;font-size:12px' in x)

        if not title_element or not company_element or not location_container:
            return None

        # Extract the job title and company name
        title = title_element.get_text(strip=True)
        company = company_element.get_text(strip=True)

        # Extract the location information from all relevant spans
        location_spans = location_container.find_all('span', style=lambda x: x and 'vertical-align:middle' in x)

        # Initialize variables
        workplace = ''
        location = ''

        # Assign values based on the number of spans found
        if len(location_spans) >= 1:
            workplace = location_spans[0].get_text(strip=True)
        if len(location_spans) >= 2:
            location = location_spans[1].get_text(strip=True)

        return {
            'title': title,
            'company': company,
            'workplace': workplace,
            'location': location,
            'url': job_url
        }
