import json
import time
import openai
from tqdm import tqdm

from src.settings import news_api_key, webhook_url
from src.utils import (
    get_completion,
    fetch_news,
    send_to_slack
)
import logging
format_log = '%(asctime)s - %(message)s'
logging.basicConfig(
    format=format_log,
    level=logging.INFO,
    datefmt='%m/%d/%Y%I:%M:%S %p'
)
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)


def main(companies, news_api_key, webhook_url, n=3):

    for company in tqdm(companies):
        logger.info('====================== {} ======================'.format(company))
        parameters['q'] = company

        news = fetch_news(news_api_key, parameters)
        for article in news[0:n]:

            logger.info('==== Processing news ====')

            content = article

            prompt = f"""
            Identify the following items from the new text: 
            - Sentiment (Excellent news, Good news, Bad news)
    
            The news is delimited with triple backticks. \
            Format your response as a JSON object with the following format: 
                "title": title,
                "source": source,
                "publishedAt": published_at,
                "url": url,
                "sentiment": sentiment,
                "summary": summary,
            Make your response as short as possible.
    
            Review text: '''{content}'''
            """
            data = json.loads(get_completion(prompt))

            emoji_dict = {"Good news": ":grinning:", "Bad news": ":disappointed:", "Excellent news": ":star-struck:"}
            sentiment_dict = {"Good news": "Rocket Fuel", "Bad news": "Smooth Sailing", "Excellent news": "Stormy Weather"}
            sentiment_emoji = emoji_dict.get(data['sentiment'], ':robot_face:')
            sentiment_label = sentiment_dict.get(data['sentiment'], ':robot_face:')

            slack_message = f"""
            {sentiment_emoji} *{data['title']}* :point_right: {data['url']}
            Sentiment: {sentiment_label} {sentiment_emoji}
            Source: {data['source']} 
            Published at: {data['publishedAt']} 

            :memo: Summary: {data['summary']} 
            """

            send_to_slack(webhook_url, slack_message)

            time.sleep(30)


if __name__=='__main__':
    companies = [
        '"Google"',
        '"Facebook"',
        '"OpenAI"',
        '"Amazon"'
    ]

    parameters = {
        'sortBy': 'popularity',
        'from_param': '2023-05-08',
        'language': 'en',
        'sources': 'TechCrunch'
    }

    main(companies, news_api_key, webhook_url)
