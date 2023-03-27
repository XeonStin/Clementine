import logging
import asyncio

import chat_utilities


logging.basicConfig(level=logging.INFO)


async def work():
    # 每 60s 请求一次趣闻
    while True:
        logging.info('Send fact request')
        chat_utilities.fact()
        await asyncio.sleep(60)


if __name__ == '__main__':
    asyncio.run(work())
