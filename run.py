import asyncio
import logging

from core import start_bot

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(start_bot())
