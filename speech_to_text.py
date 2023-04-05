import logging

import speech_recognition as sr
import zhconv
from zhon import hanzi

import chat_utilities
from config import OPENAI_API_KEY, MICROPHONE_DEVICE_INDEX, YOUR_NAME


logging.basicConfig(level=logging.INFO)
recognizer = sr.Recognizer()
recognizer.energy_threshold = 200       # 语音检测阈值，需要根据环境情况修改
recognizer.dynamic_energy_threshold = False     # 关闭自适应阈值调节，因为不太好用


while True:
    with sr.Microphone(device_index=MICROPHONE_DEVICE_INDEX) as source:
        # recognizer.adjust_for_ambient_noise(source, duration=1)   # 自适应阈值调节，不太好用
        print(f'Current energy threshold: {recognizer.energy_threshold}')
        print("Say something please!")
        audio = recognizer.listen(source)
        logging.info('Speech received.')

    try:
        # text = recognizer.recognize_whisper_api(audio, api_key=OPENAI_API_KEY, prompt='以下是普通话的句子。')
        text = recognizer.recognize_whisper_api(audio, api_key=OPENAI_API_KEY).strip()
        if text != '':
            text = zhconv.convert(text, 'zh-cn')
            if text[-1] not in hanzi.stops and text[-1] not in ('.', '!', '?'):
                text += '。'
            logging.info(f"Whisper API thinks you said:\n{text}")
            chat_utilities.send(f'“{YOUR_NAME}”说：{text}')

    except sr.RequestError as e:
        logging.info("Could not request results from Whisper API")
    