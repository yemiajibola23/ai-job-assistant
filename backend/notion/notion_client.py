from notion_client import Client
import os
from dotenv import load_dotenv

load_dotenv()

# print("Working directory:", os.getcwd())
# print("File exists:", os.path.isfile(".env"))

def get_notion_client() -> Client:
    NOTION_API_KEY=  os.getenv("NOTION_TOKEN")
    if NOTION_API_KEY is None:
        raise EnvironmentError("No Notion API Key found")

    # print("Token loaded:", NOTION_API_KEY[:10], "...")  # mask for safety
    return Client(auth=NOTION_API_KEY)
