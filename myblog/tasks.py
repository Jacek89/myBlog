from threading import Thread
from flask import current_app
from flask_mail import Message
from myblog.extensions import mail
import redis
import os
import requests
import json

r = redis.from_url(os.environ.get("REDIS_URL"))


def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)


def send_mail(subject, to, body):
    app = current_app._get_current_object()
    message = Message(subject, recipients=[to])
    message.body = body
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr


def get_sidebar_news():
    if not r.exists("sidebar_news"):
        news_param = {
            "apiKey": os.environ.get("SIDEBAR_NEWS_API_KEY"),
            "country": "pl",
            "category": os.environ.get("SIDEBAR_NEWS_CATEGORY"),
            "pageSize": os.environ.get("SIDEBAR_NEWS_AMOUNT")
        }
        try:
            response = requests.get(url="https://newsapi.org/v2/top-headlines", params=news_param)
            response.raise_for_status()
            news_data = response.json()
            list_of_articles = news_data["articles"][:5]
            parsed_data = [{'title': article['title'], 'url': article['url']} for article in list_of_articles]
            r.setex("sidebar_news", 3 * 60 * 60, json.dumps(parsed_data))
        except:
            r.setex("sidebar_news", 60 * 60, json.dumps("fail"))
    try:
        return json.loads(r.get("sidebar_news").decode('utf-8'))
    except json.JSONDecodeError:
        return r.get("sidebar_news").decode('utf-8')
