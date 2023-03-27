# Clementine

基于 ChatGPT 的直播机器人，可以：

* 语音交互：使用 speech_recognition、Whisper 语音转文字输入，使用 pyttsx3、有道 API 文字转语音输出

* 可用于 OBS 捕捉的逐词更新实时字幕网页：逐词更新功能基于 pyttsx3

* 读取 Bilibili 弹幕：功能来自于 [blivedm](https://github.com/xfgryujk/blivedm)。

## 依赖

flask, flask_cors, openai-python, pyttsx3, python-vlc, VLC播放器, speech_recognition, zhconv, zhon, blivedm 依赖库（见 [blivedm](https://github.com/xfgryujk/blivedm)）

注：

1. `pyttsx3/drivers/sapi5.py` 存在无法逐词更新的 bug，需要用 `./edited_files/sapi5.py` 替换对应文件

1. `speech_recognition` 存在无法传递 Whisper API Prompt 的 bug，需要用 `./edited_files/audio.py`, `./edited_files/whisper.py` 替换对应文件

## 配置

将 `./config_example.py` 重命名为 `config.py` 并修改

根据 `./tools/list_microphone_names.py` 的结果设置 `speect_to_text.py`

`OPENAI_API_KEY` 填写从 [Open AI](https://platform.openai.com/account/api-keys) 获取的 API Key

## 使用

启动核心程序 `./main.py`

如果需要实时字幕，在浏览器或 OBS 浏览器源中打开字幕 `./subtitle.html`

如果要手动输入对话文字，启动控制台 `./console.html`

如果要与直播间弹幕交互，启动 `./danmaku.py`

如果要与语音交互，启动 `./speect_to_text.py`

如果要隔段时间说点趣闻，启动 `./fact.py` 或访问 `核心程序服务器地址:端口/chat`

如果要访问历史聊天记录，访问 `核心程序服务器地址:端口/history`

如果要清除历史聊天记录，重启核心程序或访问 `核心程序服务器地址:端口/clear`

可以使用批处理文件（如 `./run.bat`）一次启动若干程序

---

By Xeon Stin

XeonStin@126.com
