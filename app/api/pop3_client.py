import poplib
from email import parser as email_parser
from app.parsers.builtin_jobs import BuiltinJobsParser  # Import specific parsers


class POP3Client:
    def __init__(self, config, email_type):
        self.pop_server = config.get('POP_SERVER')
        self.pop_port = config.get('POP_PORT')
        self.pop_username = config.get('POP_USERNAME')
        self.pop_password = config.get('POP_PASSWORD')

        # Initialize connection to the POP3 server
        self.mailbox = poplib.POP3_SSL(self.pop_server, self.pop_port)
        self.mailbox.user(self.pop_username)
        self.mailbox.pass_(self.pop_password)

        # Set the parser for the body of email based on email type
        self.body_parser = self.get_body_parser(email_type)

    def get_body_parser(self, email_type):
        """Returns the correct parser based on email type."""
        if email_type == 'builtin_jobs':
            return BuiltinJobsParser()
        # Add more body parsers here if needed for other email types
        else:
            raise ValueError(f"No parser found for email type: {email_type}")

    def fetch_emails(self):
        """Fetches emails from the POP3 server and uses the appropriate parser."""
        # Get the number of messages in the mailbox
        num_messages = len(self.mailbox.list()[1])
        print(f"Number of messages: {num_messages}")

        email_list = []
        for i in range(1, num_messages + 1):
            print(f"Parsing email {i}...")
            self.body_parser.parse(email_list, i)
        return email_list

    def parse(self, email_list, i):
        """Retrieves and parses the email using the selected parser."""
        raw_email = b"\n".join(self.mailbox.retr(i)[1])  # Retrieve raw email data
        parsed_email = email_parser.BytesParser().parsebytes(raw_email)

        # Extract metadata like subject
        subject = parsed_email['subject']
        print(f"Subject: {subject}")

        # Use the specific body parser for email body content
        parsed_body = self.body_parser.parse_email(parsed_email)
        email_list.append({
            'subject': subject,
            'parsed_body': parsed_body
        })

    def logout(self):
        """Logs out of the POP3 server."""
        self.mailbox.quit()
