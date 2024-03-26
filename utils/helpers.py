from loguru import logger
from settings import RETRY_COUNT
from utils.sleeping import sleep
import traceback
import pandas as pd
from config import PROGRESS_PATH
from settings import CHECK_QUESTS_PROGRESS
from main import transaction_lock
from functools import wraps


def retry(func):
    @wraps(func)
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


def quest_checker(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if CHECK_QUESTS_PROGRESS:
            with transaction_lock:
                progress = pd.read_excel(PROGRESS_PATH, index_col=0)
            account = args[0]
            module_name = func.__name__
            wallet = account.address.lower()

            try:
                status = progress.loc[wallet, module_name]
            except KeyError:
                logger.error(f"[{account.account_id}][{account.address}] Progress not found")
                from traceback import print_exc
                print_exc()
                status = False
            if not status:
                result = await func(*args, **kwargs)
                if result:
                    with transaction_lock:
                        progress.loc[wallet, module_name] = True
                        progress.fillna(False).to_excel(PROGRESS_PATH)
                return result
            else:
                logger.warning(f"[{account.account_id}][{account.address}] Module {module_name} already complete. "
                               f"Skip module")
                return -1
        else:
            result = await func(*args, **kwargs)
            return result

    return wrapper
