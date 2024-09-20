import os
import sys
from pprint import pprint

from notion_client import Client, APIResponseError

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    print("Could not load .env because python-dotenv not found.")
else:
    load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")

while NOTION_TOKEN == "":
    print("NOTION_TOKEN not found.")
    NOTION_TOKEN = input("Enter your integration token: ").strip()

# Initialize the client
notion = Client(auth=NOTION_TOKEN)

# list_users_response = notion.users.list()
# pprint(list_users_response)

# Search for an item
print("\nSearching for the word 'People' ")
results = notion.search(query="People").get("results")
print(len(results))

if results:
    result = results[0]
    print(f"The result is a {result['object']}")
    pprint(result["properties"])
else:
    print("No results found for your query.")
    sys.ext(0)

database_id = result["id"]  # store the database id in a variable for future use

# Create a new page
your_name = input("\n\nEnter your name: ")
gh_uname = input("Enter your github username: ")
new_page = {
    "Name": {"title": [{"text": {"content": your_name}}]},
    "Tags": {"type": "multi_select", "multi_select": [{"name": "python"}]},
    "GitHub": {
        "type": "rich_text",
        "rich_text": [
            {
                "type": "text",
                "text": {"content": gh_uname},
            },
        ],
    },
}

# Try to create a new page in Notion
try:
    notion.pages.create(parent={"database_id": database_id}, properties=new_page)
    print("You were added to the People database!")
except APIResponseError as e:  # Catch the correct error
    print(f"Error creating the page: {e}")
