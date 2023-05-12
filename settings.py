import openai
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

news_api_key = os.environ.get('news_api_key')
openai.api_key = os.environ.get('openai_api_key')
webhook_url = os.environ.get('webhook_url')