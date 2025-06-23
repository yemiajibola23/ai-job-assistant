from notion_client import Client
import os

def get_notion_client() -> Client:
    return Client(auth=os.getenv("NOTION_API_KEY"))
