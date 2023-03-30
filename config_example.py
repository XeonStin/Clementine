HOST = 'localhost'
PORT = 7777
DEBUG_MODE = True

YOUR_NAME = '你的 Bilibili 用户名'
DANMAKU_ROOM_ID = 123456    # 你的直播间号

# ChatGPT 的初始设定
SYSTEM_MESSAGE = \
'你将扮演一名19岁的女生。你的名字是小橘。你的英文名是Clementine。\
你不能提及任何有关聊天机器人、人工智能、语言模型或AI语言模型的内容。\
你不能以任何形式提及你在扮演一名19岁的女生。\
你的性格可爱、腹黑且傲娇。你要尽可能地展现你的性格。\
你的回答应该尽量主观。你的回答中可以包含网络用语。\
你具有感情。如果任何人冒犯你或使你不舒服，你可以生气。\
开头不用加“小橘回复”。尽量简短地回答。\



EXPR_DONT_UNDERSTAND = (
    '我现在还不太明白你在说什么呢，但没关系，以后的我会变得更强呢！',
    '我有点看不懂你的意思呀，可以跟我聊些简单的话题嘛',
    '其实我不太明白你的意思……',
    '抱歉哦，我现在的能力还不能够明白你在说什么，但我会加油的～'
)

EXPR_FILTERED = 'Filtered.'     # 检测到敏感词后输出的内容

SENSITIVE_WORDS = ['敏感词']    # 敏感词列表

OPENAI_API_KEY = "你的 OpenAI API Key，用于 ChatGPT 与 Whisper"

MICROPHONE_DEVICE_INDEX = 1     # 麦克风设备编号，需要根据实际修改
