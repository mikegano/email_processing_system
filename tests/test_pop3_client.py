import unittest
from app.email_client.pop3_client import POP3Client
from app.config import Config


class TestPOP3Client(unittest.TestCase):

    def setUp(self):
        """Set up configuration and POP3Client before each test."""
        # Load the real configuration from the .env file
        self.config = Config.load_config()
        self.client = POP3Client(self.config)

    def tearDown(self):
        """Logout from the POP3 server after each test."""
        self.client.logout()

    def test_pop3_connection(self):
        """Test that the connection to the POP3 server works."""
        try:
            # If the connection is successful, fetch emails
            emails = self.client.fetch_emails()

            # Check if we received a list of emails (even if it's empty)
            self.assertIsInstance(emails, list)
            print(f"Number of emails fetched: {len(emails)}")

        except Exception as e:
            self.fail(f"POP3 connection or email fetching failed: {e}")

    def test_fetch_emails(self):
        """Test fetching emails from the POP3 server."""
        emails = self.client.fetch_emails()

        if emails:
            # Validate that the subject of the first email is a string
            self.assertIsInstance(emails[0], str)
            print(f"First email subject: {emails[0]}")
        else:
            # If no emails were fetched, this is still valid
            print("No emails found.")
            self.assertEqual(len(emails), 0)


if __name__ == "__main__":
    unittest.main()
