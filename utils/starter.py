from utils.catizen import CatizenBot
from asyncio import sleep
from random import uniform
from data import config
from utils.core import logger
import datetime
import pandas as pd
from utils.core.telegram import Accounts
import asyncio
from aiohttp.client_exceptions import ContentTypeError


async def start(thread: int, session_name: str, phone_number: str, proxy: [str, None]):
    catizen = CatizenBot(session_name=session_name, phone_number=phone_number, thread=thread, proxy=proxy)
    account = session_name + '.session'

    await sleep(uniform(*config.DELAYS['ACCOUNT']))

    attempts = 3
    while attempts:
        try:
            await catizen.login()
            logger.success(f"Thread {thread} | {account} | Login")
            break
        except Exception as e:
            logger.error(f"Thread {thread} | {account} | Left login attempts: {attempts}, error: {e}")
            await asyncio.sleep(uniform(*config.DELAYS['RELOGIN']))
            attempts -= 1
    else:
        logger.error(f"Thread {thread} | {account} | Couldn't login")
        await catizen.logout()
        return