import poplib
from email import parser


class POP3Client:
    def __init__(self, config):

        self.pop_server = config.get('POP_SERVER')
        self.pop_port = config.get('POP_PORT')
        self.pop_username = config.get('POP_USERNAME')
        self.pop_password = config.get('POP_PASSWORD')

        # Initialize connection to the POP3 server
        self.mailbox = poplib.POP3_SSL(self.pop_server, self.pop_port)
        self.mailbox.user(self.pop_username)
        self.mailbox.pass_(self.pop_password)

    def fetch_emails(self):
        """Fetches emails from the POP3 server."""
        # Get the number of messages in the mailbox
        num_messages = len(self.mailbox.list()[1])
        print(f"Number of messages: {num_messages}")

        email_list = []
        for i in range(1, num_messages + 1):
            raw_email = b"\n".join(self.mailbox.retr(i)[1])  # Retrieve raw email data
            parsed_email = parser.BytesParser().parsebytes(raw_email)

            # Extract subject and other necessary details
            subject = parsed_email['subject']
            email_list.append(subject)

        return email_list

    def logout(self):
        """Logs out of the POP3 server."""
        self.mailbox.quit()


# Example usage (for testing directly, if needed)
if __name__ == "__main__":
    config = {
        'POP_SERVER': 'mail2.nextmill.net',
        'POP_PORT': 995,
        'POP_USERNAME': '',
        'POP_PASSWORD': ''
    }

    client = POP3Client(config)
    emails = client.fetch_emails()

    if emails:
        print(f"Successfully retrieved {len(emails)} emails.")
        for idx, email_subject in enumerate(emails[:5], 1):
            print(f"Email {idx}: {email_subject}")
    else:
        print("No emails found.")

    client.logout()
