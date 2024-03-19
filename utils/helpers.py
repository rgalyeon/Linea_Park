from loguru import logger
from settings import RETRY_COUNT
from utils.sleeping import sleep
import traceback


def retry(func):
    async def wrapper(*args, **kwargs):
        retries = 0
        while retries <= RETRY_COUNT:
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                logger.error(f"Error | {e}")
                traceback.print_exc()
                await sleep(10, 20)
                retries += 1

    return wrapper


def remove_wallet(private_key: str):
    with open("wallets.txt", "r") as file:
        lines = file.readlines()

    with open("wallets.txt", "w") as file:
        for line in lines:
            if private_key not in line:
                file.write(line)
