import logging
import threading
from urllib import parse

from flask import Flask, make_response, request
from flask_cors import CORS
import pyttsx3
import vlc
 
from ChatGPT_API import ChatGPTConversation
from config import *


log = logging.getLogger('werkzeug')
log.disabled = True                     # 关闭请求 log

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)   # 实例化 app 对象
CORS(app, supports_credentials=True)


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
        threading.Thread.join(self)  # 等待线程执行完毕
        try:
            return self.result
        except Exception:
            return None


@app.route('/subtitle', methods=['GET','POST'])
def send_subtitle():
    # 接受字幕请求，返回字幕信息
    global subtitle_text
    return subtitle_text


def update_subtitle(text: str):
    # 更新字幕文字
    global subtitle_text
    logging.info(f'Update subtitle to:\n{text}')
    subtitle_text = text


def run_tts(text: str, start_speech_from: int=0, rate: int=180, voice_id: int=4):
    # 使用 pyttsx3 TTS 并实时逐词更新字幕
    global is_saying
    # 初始化
    # print(f'Say: {text}\nVoice: {voices[voice_id]}\nRate: {rate}\n')
    logging.info(f'Entered run_tts with text: {text}\nStart from {start_speech_from}')
    
    tts_engine = pyttsx3.init()
    tts_engine.setProperty('rate', rate)
    voices = tts_engine.getProperty('voices')
    tts_engine.setProperty('voice', voices[voice_id].id)
    tts_engine.setProperty('volume', 1)     # 打开 pyttsx3 声音

    def onStartWord(name: str, location: int, length: int):
        subtitle = text[0: start_speech_from+location+length]
        update_subtitle(subtitle)
        # print(subtitle)

    tts_engine.connect('started-word', onStartWord)
    tts_engine.say(text[start_speech_from:])
    tts_engine.runAndWait()
    update_subtitle(text)
    '''time.sleep(1)
    update_subtitle('')'''
    is_saying = False   # 解除 pyttsx3 占用


def play_youdao_audio(text: str):
    # 调用有道 API 生成语音，并用 VLC 播放
    url = f'http://tts.youdao.com/fanyivoice?word={parse.quote(text)}&le=zh&keyfrom=speaker-target'
    p = vlc.MediaPlayer(url)
    p.play()


def run_tts_youdao(text: str, start_speech_from: int=0):
    # 使用调用有道 API TTS，并用 pyttsx3 实时逐词更新字幕
    global is_saying
    logging.info(f'Entered run_tts_youdao with text: {text}\nStart from {start_speech_from}')
    
    MyThread(play_youdao_audio, (text,)).start()
    tts_engine = pyttsx3.init()
    tts_engine.setProperty('rate', 180)
    voices = tts_engine.getProperty('voices')
    tts_engine.setProperty('voice', voices[4].id)
    tts_engine.setProperty('volume', 0)     # 关闭 pyttsx3 声音

    def onStartWord(name: str, location: int, length: int):
        subtitle = text[0: start_speech_from+location+length]
        update_subtitle(subtitle)

    tts_engine.connect('started-word', onStartWord)
    tts_engine.say(text[start_speech_from:])
    tts_engine.runAndWait()
    update_subtitle(text)
    is_saying = False


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
    global is_saying
    # 判断 pyttsx3 占用情况
    if is_saying:
        return 'Busy'
    is_saying = True

    if request.method == 'GET':
        # 无参数 GET 请求，找个话题
        logging.info(f'Entering with GET')
        text = '有什么趣闻吗？'

    else:
        # 带参数 POST 请求
        try:
            logging.info(f'Entering with POST')
            logging.info(f'Data: {request.get_data()}')
            text = request.json.get('data')
            logging.info(f'POST content: \n{text}')
        except:
            logging.error(f'Error proceeding data: {request.get_data()}')
            return f'Error proceeding data: {request.get_data()}'

    answer = get_answer(text)
    MyThread(run_tts_youdao, (answer, )).start()
    return answer


'''@app.route('/chat_readback', methods=['POST'])
def answer_chat() -> str:
    # 带读弹幕的回复
    global is_saying
    if is_saying:
        return 'Busy'
    is_saying = True

    try:
        logging.info(f'Entering with POST')
        logging.info(f'Data: {request.get_data()}')
        text = request.json.get('data')
        logging.info(f'POST content: \n{text}')
    except:
        logging.error(f'Error proceeding data: {request.get_data()}')
        return f'Error proceeding data: {request.get_data()}'

    t1 = MyThread(run_tts, (text, 0, 220))
    t2 = MyThread(get_answer, (text, ))

    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    answer = t2.get_result()

    run_tts(text + answer, len(text))
    # run_tts(text + answer, start_speech_from=len(text))

    is_saying = False
    return answer'''


@app.route('/clear', methods=['GET','POST'])
def clear():
    # 清除聊天记录
    conversation.clear()
    logging.info(f'History cleared.')


@app.route('/history', methods=['GET','POST'])
def history():
    # 调取聊天记录
    logging.info(f'History returned.')
    history = str(conversation.get_history())
    return history


if __name__ == '__main__':
    app.run(host  = HOST,   # 任何ip都可以访问
            port  = PORT,          # 端口
            debug = DEBUG_MODE)
