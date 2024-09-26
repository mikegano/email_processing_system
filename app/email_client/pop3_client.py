import os
import time
import logging
import poplib
from email import parser as email_parser

logger = logging.getLogger(__name__)

class POP3EmailClient:
    def __init__(self, email_config):
        """Connect to email server."""
        self.server = email_config['server']
        self.port = email_config['port']
        self.username = email_config['username']
        self.password = email_config['password']

        try:
            self.mailbox = poplib.POP3_SSL(self.server, self.port)
            self.mailbox.user(self.username)
            self.mailbox.pass_(self.password)
            logger.info(f"Connected to {self.server} on port {self.port} as {self.username}")
        except poplib.error_proto as e:
            logger.error(f"Failed to connect or authenticate: {e}")
            raise ConnectionError(f"Failed to connect or authenticate: {e}")

    def fetch_emails(self):
        """Fetches emails from the POP3 server and uses the appropriate parser."""
        num_messages = len(self.mailbox.list()[1])
        logger.info(f"Number of messages: {num_messages}")

        email_list = []
        for i in range(1, num_messages + 1):
            logger.info(f"Retrieving email {i}")
            try:
                raw_email = b"\n".join(self.mailbox.retr(i)[1])
                parsed_email = email_parser.BytesParser().parsebytes(raw_email)
                email_list.append(parsed_email)
            except Exception as e:
                logger.error(f"Error retrieving or parsing email {i}: {e}")
                continue
        return email_list

    def save_email(self, email):
        """Save email to the parsed_email folder with a timestamped filename."""
        try:
            # Get the current timestamp to use as a filename
            timestamp = time.strftime("%Y%m%d_%H%M%S")

            # Construct the filename using the timestamp
            email_file_name = f"{timestamp}.eml"

            # Adjust the file path
            email_file_path = os.path.join(os.path.dirname(__file__), "../../data/parsed_emails", email_file_name)

            # Write the email content to the file
            with open(email_file_path, 'w') as email_file:
                email_file.write(email.as_string())
                logger.info(f"Email saved successfully as {email_file_name}")

            return True
        except Exception as e:
            logger.error(f"Failed to save email: {e}")
            return False

    def delete_email(self, index):
        """Deletes an email from the POP3 server by index."""
        try:
            self.mailbox.dele(index)
            logger.info(f"Email {index} successfully deleted from the server.")
        except Exception as e:
            logger.error(f"Failed to delete email {index}: {e}")

    def logout(self):
        """Logs out of the POP3 server."""
        self.mailbox.quit()
