import requests
import logging

from config import HOST, PORT


CHATTER_URL = f'http://{HOST}:{PORT}/chat'
proxies = {"http": None, "https": None}


def send(text: str):
    content = {'data': text}
    try:
        reply = str(requests.post(url = CHATTER_URL, json = content, proxies=proxies).content, 'utf-8')
        logging.info(f'Received: \n{reply}')
    except:
        logging.error('Error occured when sending text to Chatter')


def fact():
    try:
        reply = str(requests.get(url = CHATTER_URL, proxies=proxies).content, 'utf-8')
        logging.info(f'Received: \n{reply}')
    except:
        logging.error('Error occured when sending text to Chatter')
