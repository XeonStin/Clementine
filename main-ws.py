import logging
import threading
from urllib import parse

from flask import Flask, make_response, request
from flask_socketio import SocketIO
from flask_cors import CORS
 
from ChatGPT_API import ChatGPTConversation
from config import *


'''log = logging.getLogger('werkzeug')
log.disabled = True                     # 关闭请求 log'''

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)                   # 实例化 app 对象
CORS(app, supports_credentials=True)
socketio = SocketIO(app, cors_allowed_origins='*')

socketio_namespace = '/tts'

conversation = ChatGPTConversation(SYSTEM_MESSAGE)
subtitle_text = ''
is_saying = False


class MyThread(threading.Thread):       # 用于带返回值的线程
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        threading.Thread.join(self)     # 等待线程执行完毕
        try:
            return self.result
        except Exception:
            return None


@app.after_request
def af_request(resp):     
    """
    #请求钩子，在所有的请求发生后执行，加入headers。
    :param resp:
    :return:
    """
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp


@socketio.on('connect', namespace=socketio_namespace)
def connected_msg():
    logging.info('SocketIO: Client connected')


@socketio.on('disconnect', namespace=socketio_namespace)
def disconnect_msg():
    logging.info('SocketIO: Client disconnected')


@socketio.on('tts_finished', namespace=socketio_namespace)
def tts_finished(message):
    logging.info('TTS finished')
    global is_saying
    is_saying = False


def get_answer(text: str) -> str:
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


@app.route('/chat', methods=['GET', 'POST'])
def answer() -> str:
    '''global is_saying
    # 判断 pyttsx3 占用情况
    if is_saying:
        return 'Busy'
    is_saying = True'''

    if request.method == 'GET':
        # 无参数 GET 请求，找个话题
        logging.info(f'Entering with GET')
        text = '有什么趣闻吗？'

    else:
        # 带参数 POST 请求
        try:
            logging.info(f'Entering with POST')
            logging.info(f'Data: {request.get_data()}')
            text = request.json.get('data').strip()
            logging.info(f'POST content: { text }')
        except:
            logging.error(f'Error proceeding data: {request.get_data()}')
            return f'Error proceeding data: {request.get_data()}'

    answer = get_answer(text)
    logging.info(f'SocketIO send {answer}')
    socketio.emit("tts", {'text': answer}, namespace=socketio_namespace)
    return answer


@app.route('/clear', methods=['GET','POST'])
def clear():
    # 清除聊天记录
    conversation.clear()
    logging.info(f'History cleared.')
    return 'History cleared.'


@app.route('/history', methods=['GET','POST'])
def history():
    # 调取聊天记录
    logging.info(f'History returned.')
    history = str(conversation.get_history())
    return history


if __name__ == '__main__':
    socketio.run(app, host  = HOST,   # 任何ip都可以访问
            port  = PORT,          # 端口
            debug = DEBUG_MODE)
