import requests
from newsapi import NewsApiClient
import openai
import json


def fetch_news(api_key, parameters):
    """
    Fetch news articles from NewsAPI.

    Args:
        api_key (str): API key for NewsAPI.
        parameters (dict): Dictionary of parameters to pass to NewsAPI.

    Returns:
        list: List of news articles.
    """
    newsapi = NewsApiClient(api_key=api_key)
    top_headlines = newsapi.get_everything(
        q=parameters['q'],
        sources=parameters['sources'],
        from_param=parameters['from_param'],
        language=parameters['language'],
        sort_by=parameters['sortBy'],
    )
    return top_headlines['articles']


def get_completion(prompt, model="gpt-3.5-turbo"):
    """
    Get completion from OpenAI GPT-3 model.

    Args:
        prompt (str): Prompt for the model.
        model (str): Model to use. Default is 'gpt-3.5-turbo'.

    Returns:
        str: Model's response.
    """
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]


def send_to_slack(webhook_url, text):
    """
    Send a message to a Slack channel.

    Args:
        webhook_url (str): Slack incoming WebHook URL.
        text (str): Message text.

    Returns:
        Response object from requests.post.
    """

    headers = {'Content-Type': 'application/json'}
    data = {'text': text}


    response = requests.post(webhook_url, headers=headers, data=json.dumps(data))
    return response