import poplib
from email import parser
from config.config import Config  # Import the config

# Load configuration
config = Config.load_config()

pop3_server = config['POP_SERVER']
pop3_port = config['POP_PORT']
pop_username = config['POP_USERNAME']
pop_password = config['POP_PASSWORD']

# Initialize connection to the POP3 server
mailbox = poplib.POP3_SSL(pop3_server, pop3_port)

# Authenticate
mailbox.user(pop_username)
mailbox.pass_(pop_password)

# Get the number of messages in the mailbox
num_messages = len(mailbox.list()[1])

print(f"Number of messages: {num_messages}")

# Fetch and print the first email
for i in range(1, num_messages + 1):
    raw_email = b"\n".join(mailbox.retr(i)[1])  # Retrieve raw email data
    parsed_email = parser.BytesParser().parsebytes(raw_email)

    # Print email subject
    print(f"Subject: {parsed_email['subject']}")

# Close the connection
mailbox.quit()
