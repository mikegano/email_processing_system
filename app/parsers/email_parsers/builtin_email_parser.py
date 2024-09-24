from bs4 import BeautifulSoup
from ...storage.notion_api import NotionClient
from ...parsers.base_parser import BaseParser
from ...models.job import Job

class BuiltInEmailParser(BaseParser):
    def __init__(self, notion_config):
        self.notion_inserter = NotionClient(notion_config)

    def _parse_html_body(self, html_body):
        """Parse the HTML body for job information."""
        soup = BeautifulSoup(html_body, 'html.parser')
        job_elements = soup.find_all('td', style=lambda x: x and 'font-family:Verdana' in x)

        if not job_elements:
            return []

        jobs = []
        for job_element in job_elements:
            job_info = self._get_job_info(job_element)
            if job_info:
                jobs.append(job_info)

        return jobs

    def _get_job_info(self, job_element):
        """Extract job information from a job element."""
        a_tag = job_element.find('a', href=True)
        if not a_tag:
            return None
        job_url = a_tag['href']

        title_element = job_element.find('div', style=lambda x: x and 'font-size:20px' in x)
        company_element = job_element.find('div', style=lambda x: x and 'font-size:16px' in x)

        # Find the parent div that contains the location info
        # location_container = job_element.find('div', style=lambda x: x and 'margin-bottom:4px;font-size:12px' in x)
        container_match = 'margin-bottom:4px;font-size:12px'
        location_container = job_element.find('div', style=lambda x: x and container_match in x)

        if not title_element or not company_element or not location_container:
            return None

        title = title_element.get_text(strip=True)
        company = company_element.get_text(strip=True)

        # Extract the location information from all relevant spans
        # location_spans = location_container.find_all('span', style=lambda x: x and 'vertical-align:middle' in x)
        spans_match = 'vertical-align:middle'
        location_spans = location_container.find_all('span', style=lambda x: x and spans_match in x)

        workplace = ''
        location = ''

        # Assign values based on the number of spans found
        if len(location_spans) >= 1:
            workplace = location_spans[0].get_text(strip=True)
        if len(location_spans) >= 2:
            location = location_spans[1].get_text(strip=True)

        return Job(
            title=title,
            company=company,
            location=location,
            url=job_url,
            workplace=workplace
        )
