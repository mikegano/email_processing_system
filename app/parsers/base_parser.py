from abc import ABC, abstractmethod

class BaseParser(ABC):
    @abstractmethod
    def _parse_html_body(self, html_body):
        """Parse the HTML body and extract job details."""
        pass

    @abstractmethod
    def _get_job_info(self, job_element):
        """Extract job information from an HTML element."""
        pass

    @abstractmethod
    def can_parse(self, email):
        """Determine if this parser can handle the given email."""
        pass

    def parse(self, parsed_email):
        """Parse the email content."""
        if not parsed_email.is_multipart():
            return {}

        for part in parsed_email.walk():
            if self._is_html_part(part):
                html_body = self._get_html_body(part)
                return self._parse_html_body(html_body)
        return {}

    def _is_html_part(self, part):
        """Check if the email part is HTML."""
        return part.get_content_type() == "text/html"

    def _get_html_body(self, part):
        """Extract the HTML body content from an email part."""
        return part.get_payload(decode=True).decode()
