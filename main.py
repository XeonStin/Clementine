import logging

from flask import Flask, make_response, request, render_template
from flask_socketio import SocketIO
from flask_cors import CORS
 
from ChatGPT_API import ChatGPTConversation
from chat_utilities import get_answer
from config import HOST, PORT, DEBUG_MODE, SYSTEM_MESSAGE, YOUR_NAME


logging.basicConfig(level=logging.INFO)

app = Flask(__name__)                   # 实例化 app 对象
CORS(app, supports_credentials=True)
socketio = SocketIO(app, cors_allowed_origins='*')
socketio_namespace = '/tts'

conversation = ChatGPTConversation(SYSTEM_MESSAGE)


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
def socketio_connected():
    logging.info('SocketIO: Client connected')


@socketio.on('disconnect', namespace=socketio_namespace)
def socketio_disconnect():
    logging.info('SocketIO: Client disconnected')


@socketio.on('tts_finished', namespace=socketio_namespace)
def tts_finished(message):
    logging.info('TTS finished')


@app.route('/chat', methods=['GET', 'POST'])
def chat() -> str:
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

    answer = get_answer(text, conversation)
    logging.info(f'SocketIO send {answer}')
    socketio.emit("tts", {'text': answer}, namespace=socketio_namespace)
    return answer


@app.route('/chat_from_console', methods=['POST'])
def chat_from_console() -> str:
    # 带参数 POST 请求
    try:
        logging.info(f'Entering with POST')
        logging.info(f'Data: {request.get_data()}')
        text = request.json.get('data').strip()
        text = f'“{YOUR_NAME}”说：{text}'
        logging.info(f'POST content: { text }')
    except:
        logging.error(f'Error proceeding data: {request.get_data()}')
        return f'Error proceeding data: {request.get_data()}'

    answer = get_answer(text, conversation)
    logging.info(f'SocketIO send {answer}')
    socketio.emit("tts", {'text': answer}, namespace=socketio_namespace)
    return answer


@app.route('/clear', methods=['GET','POST'])
def clear():
    # 清除聊天记录
    conversation.clear()
    logging.info(f'History cleared.')
    return 'History cleared.'


@app.route('/subtitle', methods=['GET'])
def subtitle():
    return render_template('tts-and-subtitle.html')

    
@app.route('/chat_console', methods=['GET'])
def console():
    return render_template('console.html')


@app.route('/history', methods=['GET','POST'])
def history():
    # 调取聊天记录
    logging.info(f'History returned.')
    history = str(conversation.get_history())
    return history


if __name__ == '__main__':
    socketio.run(app, host=HOST, port=PORT, debug=DEBUG_MODE)
