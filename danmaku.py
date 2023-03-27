import asyncio
import logging

import blivedm

import chat_utilities
from config import DANMAKU_ROOM_ID


logging.basicConfig(level=logging.INFO)


class MyHandler(blivedm.BaseHandler):
    # 添加自定义回调
    async def _on_danmaku(self, client: blivedm.BLiveClient, message: blivedm.DanmakuMessage):
        text = f'“{message.uname}”说：{message.msg}'
        logging.info(text)
        chat_utilities.send(text)


    async def _on_gift(self, client: blivedm.BLiveClient, message: blivedm.GiftMessage):
        text = f'“{message.uname}”送给了你{message.num}个{message.gift_name}'
        logging.info(text)
        chat_utilities.send(text)


    async def _on_super_chat(self, client: blivedm.BLiveClient, message: blivedm.SuperChatMessage):
        text = f'“{message.uname}”说：{message.message}'
        logging.info(text)
        chat_utilities.send(text)


async def run_single_client():
    """
    演示监听一个直播间
    """
    room_id = DANMAKU_ROOM_ID    # 直播间ID的取值看直播间URL
    # 如果SSL验证失败就把ssl设为False，B站真的有过忘续证书的情况
    client = blivedm.BLiveClient(room_id, ssl=False)
    handler = MyHandler()
    client.add_handler(handler)

    client.start()
    logging.info('Danmaku is running')
    try:
        await client.join()
    finally:
        await client.stop_and_close()


async def main():
    loop = asyncio.get_event_loop()
    loop.run_forever(await run_single_client())


if __name__ == '__main__':
    asyncio.run(main())
