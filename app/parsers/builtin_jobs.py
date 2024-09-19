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

        # Example: Update based on the actual structure of your emails
        jobs = []
        job_elements = soup.find_all('div', class_='job-listing')
        for job_element in job_elements:
            title = self.get_job_title(job_element)
            description = self.get_job_description(job_element)
            jobs.append({
                'title': title,
                'description': description
            })

        return jobs

    def get_job_title(self, job_element):
        return job_element.find('h2').text if job_element.find('h2') else None

    def get_job_description(self, job_element):
        return job_element.find('p').text if job_element.find('p') else None
