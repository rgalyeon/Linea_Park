import random
import warnings
from loguru import logger

from config import LINEASCAN_URL, LINEA_API_KEYS, PROGRESS_PATH, COOPRECORDS_CONTRACT
import requests
from typing import List, Dict
import pandas as pd
from tqdm import tqdm
import time
import os
from config import (ELEMENT_CONTRACT, SATOSHI_UNIVERSE_CONTRACT, EFROGS_CONTRACT)

warnings.filterwarnings('ignore')


class LineaScan:
    def __init__(self, wallets_data):
        self.wallets_data = wallets_data

    @staticmethod
    def url_maker(module, action, **kwargs) -> str:

        url = LINEASCAN_URL + f'?module={module}' \
                              f'&action={action}' \
                              f'&apikey={random.choice(LINEA_API_KEYS)}'
        if kwargs:
            for key, value in kwargs.items():
                url += f'&{key}={value}'
        return url

    def get_wallet_transactions(self, address, proxies=None):
        url = self.url_maker('account', 'txlist', address=address)
        if proxies:
            try:
                response = requests.get(url, proxies=proxies, timeout=10)
            except:
                response = requests.get(url)
        else:
            response = requests.get(url)
        res = response.json()
        return res

    @staticmethod
    def parse_transactions(transactions: List[Dict], wallet, df: pd.DataFrame):
        df.loc[wallet, :] = False
        for tx in transactions:
            if tx['to'] == EFROGS_CONTRACT.lower():
                df.loc[wallet, 'W1 Task 5'] = True
            elif tx['to'] == SATOSHI_UNIVERSE_CONTRACT.lower():
                df.loc[wallet, 'W2 Task 1'] = True
            elif tx['to'] == ELEMENT_CONTRACT.lower() and '1ffca9db' in tx['input']:
                df.loc[wallet, 'W2 Task 2'] = True
            elif tx['to'] == '0xF502AA456C4ACe0D77d55Ad86436F84b088486F1'.lower():
                df.loc[wallet, 'W2 Task 3'] = True
            elif tx['to'] == '0x32DeC694570ce8EE6AcA08598DaEeA7A3e0168A3'.lower():
                df.loc[wallet, 'W2 Task 4'] = True
            elif tx['to'] == '0x057b0080120D89aE21cC622db34f2d9Ae9fF2BDE'.lower():
                df.loc[wallet, 'W2 Task 5'] = True
            elif tx['to'] == '0x0841479e87Ed8cC7374d3E49fF677f0e62f91fa1'.lower():
                df.loc[wallet, 'W2 Task 6'] = True
            elif tx['to'] == ELEMENT_CONTRACT.lower() and '19a747c1' in tx['input']:
                df.loc[wallet, 'W3 Task 1'] = True
            elif tx['to'] == '0xEaea2Fa0dea2D1191a584CFBB227220822E29086'.lower():
                df.loc[wallet, 'W3 Task 2'] = True
            elif tx['to'] == '0x8Ad15e54D37d7d35fCbD62c0f9dE4420e54Df403'.lower():
                df.loc[wallet, 'W3 Task 3'] = True
            elif tx['to'] == '0x3A21e152aC78f3055aA6b23693FB842dEFdE0213'.lower():
                df.loc[wallet, 'W3 Task 4'] = True
            elif tx['to'] == '0x5A77B45B6f5309b07110fe98E25A178eEe7516c1'.lower():
                df.loc[wallet, 'W3 Task 5'] = True
            elif tx['to'] == ELEMENT_CONTRACT.lower() and '2968bd75' in tx['input']:
                df.loc[wallet, 'W3 Task 6'] = True
            elif tx['to'] == COOPRECORDS_CONTRACT.lower():
                df.loc[wallet, 'W4 Task 1'] = True

    def wait_transactions(self, address, all_proxies):
        n_attemps = 10
        while n_attemps:
            proxy = random.choice(all_proxies)
            proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
            transactions = self.get_wallet_transactions(address.lower(), proxies)
            if transactions['status'] == 1:
                return transactions
            n_attemps -= 1
            time.sleep(5)

    def get_wallet_progress(self, replace=False):
        if os.path.exists(PROGRESS_PATH) and not replace:
            logger.info(f'Load progress from {PROGRESS_PATH}')
            return
        logger.info('Check quests progress from blockchain data')

        cols = ['W1 Task 5', 'W2 Task 1', 'W2 Task 2', 'W2 Task 3', 'W2 Task 4', 'W2 Task 5', 'W2 Task 6',
                'W3 Task 1', 'W3 Task 2', 'W3 Task 3', 'W3 Task 4', 'W3 Task 5', 'W3 Task 6',
                'W4 Task 1']

        df = pd.DataFrame(columns=cols)
        all_proxies = [wallet_info['proxy'] for wallet_info in self.wallets_data]
        for wallet_info in tqdm(self.wallets_data):
            address = wallet_info['address'].lower()
            proxies = {'http': f'http://{wallet_info["proxy"]}', 'https': f'http://{wallet_info["proxy"]}'}
            try:
                transactions = self.get_wallet_transactions(address, proxies)
                if transactions['status'] != '1':
                    transactions = self.wait_transactions(address, all_proxies)
            except:
                transactions = self.wait_transactions(address, all_proxies)
            try:
                if transactions['status'] == '1':
                    self.parse_transactions(transactions['result'][-100:], wallet_info['address'], df)
                else:
                    print(transactions)
            except Exception as e:
                logger.warning(f'Can not parse {address} wallet. Error: {e}')
        df.fillna(False).to_excel(PROGRESS_PATH)
