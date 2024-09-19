import poplib
from email import parser as email_parser
from app.parsers.builtin_jobs import BuiltinJobsParser  # Import specific parsers


class POP3Client:
    def __init__(self, config, email_type):
        """Connect to email server"""
        self.pop_server = config.get('POP_SERVER')
        self.pop_port = config.get('POP_PORT')
        self.pop_username = config.get('POP_USERNAME')
        self.pop_password = config.get('POP_PASSWORD')

        try:
            self.mailbox = poplib.POP3_SSL(self.pop_server, self.pop_port)
            self.mailbox.user(self.pop_username)
            self.mailbox.pass_(self.pop_password)
        except poplib.error_proto as e:
            raise ConnectionError(f"Failed to connect or authenticate: {e}")

        self.body_parser = self._get_body_parser(email_type)

    def fetch_emails(self):
        """Fetches emails from the POP3 server and uses the appropriate parser."""
        num_messages = len(self.mailbox.list()[1])
        print(f"Number of messages: {num_messages}")

        email_list = []
        for i in range(1, num_messages + 1):
            print(f"Parsing email {i}...")
            self._body_parse(email_list, i)
        return email_list

    def logout(self):
        """Logs out of the POP3 server."""
        self.mailbox.quit()

    def _get_body_parser(self, email_type):
        """Returns the correct parser based on email type."""
        if email_type == 'builtin_jobs':
            return BuiltinJobsParser()
        # Add more body parsers here if needed for other email types
        else:
            raise ValueError(f"No parser found for email type: {email_type}")

    def _body_parse(self, email_list, i):
        """Retrieves and parses the email using the selected parser."""

        try:
            raw_email = b"\n".join(self.mailbox.retr(i)[1])
            parsed_email = email_parser.BytesParser().parsebytes(raw_email)
        except Exception as e:
            print(f"Error retrieving or parsing email {i}: {e}")
            return

        # Extract metadata like subject
        subject = parsed_email.get('subject', 'No Subject')
        print(f"Subject: {subject}")

        # Use the specific body parser for email body content
        parsed_body = self.body_parser.parse_email(parsed_email)
        email_list.append({
            'subject': subject,
            'parsed_body': parsed_body
        })


