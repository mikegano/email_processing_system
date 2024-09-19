from bs4 import BeautifulSoup


class BuiltinJobsParser:
    """Parser for emails of type 'builtin_jobs'."""

    def parse_email(self, parsed_email):
        if not parsed_email.is_multipart():
            return {}

        for part in parsed_email.walk():
            if self.is_html_part(part):
                html_body = self.get_html_body(part)
                return self.parse_html_body(html_body)
        return {}

    def is_html_part(self, part):
        return part.get_content_type() == "text/html"

    def get_html_body(self, part):
        return part.get_payload(decode=True).decode()

    def parse_html_body(self, html_body):
        soup = BeautifulSoup(html_body, 'html.parser')

        jobs = []

        # Find all job blocks
        job_elements = soup.find_all('td', style=lambda x: x and 'font-family:Verdana' in x)

        for job_element in job_elements:
            job_info = self.get_job_info(job_element)
            if job_info:
                jobs.append(job_info)

        return jobs

    def get_job_info(self, job_element):
        """Extract job information from a given job_element."""

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
        remote_type = ''
        location = ''

        # Assign values based on the number of spans found
        if len(location_spans) >= 1:
            remote_type = location_spans[0].get_text(strip=True)
        if len(location_spans) >= 2:
            location = location_spans[1].get_text(strip=True)

        return {
            'title': title,
            'company': company,
            'remote_type': remote_type,
            'location': location,
            'url': job_url
        }
