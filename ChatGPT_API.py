from typing import List
import logging

import openai

from config import OPENAI_API_KEY


openai.api_key = OPENAI_API_KEY


class ChatGPTConversation:
    INSTRUCTION_DEFAULT = ''
    MAX_HISTORY_LENGTH = 20


    def __init__(self, instruction=INSTRUCTION_DEFAULT):
        self.system_message = {"role": "system", "content": instruction}
        self.history_messages =  []  # 历史消息为偶数条，不包含系统指令


    def ask(self, content: str, tip: str='') -> str:
        if not content:
            return None
        
        logging.info(f'Ask: {content}\nTip: {tip}')

        new_system_message = self.system_message
        new_system_message['content'] += tip
        
        try: 
            messages = self.history_messages + [{"role": "user", "content": content}]
            reply = self.get_ChatGPT_reply([new_system_message] + messages)
        except:
            logging.error(f'ChatGPT: No response')
            return 'ChatGPT 出现错误，请重试'

        self.history_messages = messages + [{"role": "assistant", "content": reply}]

        if len(self.history_messages) > self.MAX_HISTORY_LENGTH:
            self.history_messages = self.history_messages[2:]

        logging.info(f'ChatGPT: Reply: {reply}')
        return reply
    

    def clear(self):
        self.history_messages = []
        logging.info(f'ChatGPT: History cleared')
    

    def get_history(self):
        return str([self.system_message] + self.history_messages)


    def withdraw(self):
        if len(self.history_messages) >= 2:
            self.history_messages = self.history_messages[:-2]
        logging.info(f'ChatGPT: Last round withdrawn')

    
    def get_ChatGPT_reply(self, messages: List[dict]) -> str:
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = messages
        )
        logging.info(str(response['usage']))
        reply_message = response['choices'][0]['message']['content'].strip()

        return reply_message 
