import requests
import logging

from config import HOST, PORT, SENSITIVE_WORDS, EXPR_FILTERED


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


def get_answer(text: str, conversation) -> str:
    reply = conversation.ask(text, tip='')
    answer = ''
    if reply:
        # 判断敏感词
        for word in SENSITIVE_WORDS:
            if word in reply:
                logging.info(f'Reply contain sensitive word: {word}')
                conversation.withdraw()
                return EXPR_FILTERED
        # No problem
        answer = reply
    else:
        logging.error('Reply is None')
    
    return answer
