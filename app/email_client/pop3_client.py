import poplib
from email import parser as email_parser

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
        except poplib.error_proto as e:
            raise ConnectionError(f"Failed to connect or authenticate: {e}")

    def fetch_emails(self):
        """Fetches emails from the POP3 server and uses the appropriate parser."""
        num_messages = len(self.mailbox.list()[1])
        print(f"Number of messages: {num_messages}")

        email_list = []
        for i in range(1, num_messages + 1):
            print(f"Retrieving email {i}...")
            try:
                raw_email = b"\n".join(self.mailbox.retr(i)[1])
                parsed_email = email_parser.BytesParser().parsebytes(raw_email)
                email_list.append(parsed_email)
            except Exception as e:
                print(f"Error retrieving or parsing email {i}: {e}")
                continue
        return email_list

    def logout(self):
        """Logs out of the POP3 server."""
        self.mailbox.quit()
