import random

from loguru import logger

from config import LINEASCAN_URL, LINEA_API_KEYS, PROGRESS_PATH
import requests
from typing import List, Dict
import pandas as pd
from tqdm import tqdm
import time
import os


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
        s_universe = 'de240b2a3634fcd72919eb591a7207bddef03cd'
        df.loc[wallet, :] = False
        for tx in transactions:
            if tx['to'] == '0x6cd20be8914a9be48f2a35e56354490b80522856' and tx['methodId'] == '0xb9a2092d':
                df.loc[wallet, 'gamer_boom_proof'] = True
            elif tx['to'] == '0xc0b4ab5cb0fdd6f5dfddb2f7c10c4c6013f97bf2' and tx['methodId'] == '0x1249c58b':
                df.loc[wallet, 'gamer_boom_mint'] = True
            elif tx['to'] == '0x34be5b8c30ee4fde069dc878989686abe9884470' and tx['methodId'] == '0xe139278f':
                df.loc[wallet, 'nidum_mint'] = True
            elif tx['to'] == '0x281a95769916555d1c97036e0331b232b16edabc' and tx['methodId'] == '0xf160619b':
                df.loc[wallet, 'townstory_mint'] = True
            elif tx['to'] == '0xd41ac492fedc671eb965707d1dedad4eb7b6efc5' and tx['methodId'] == '0x48e33382':
                df.loc[wallet, 'travelbag_mint'] = True
            # Week 2
            elif tx['to'] == '0x66ccc220543b6832f93c2082edd7be19c21df6c0' and tx['methodId'] == '0xefef39a1':
                df.loc[wallet, 'abuse_world_mint'] = True
            elif tx['to'] == '0xb18b7847072117ae863f71f9473d555d601eb537' and tx['methodId'] == '0x14f710fe':
                df.loc[wallet, 'pictograph_mint'] = True
            elif tx['to'] == 'gergmemg4l4':  # todo fix
                df.loc[wallet, 'pictograph_stake'] = True
            elif tx['to'] == '0xecbee1a087aa83db1fcc6c2c5effc30bcb191589' and s_universe in tx['input']:
                df.loc[wallet, 'satoshi_universe_mint'] = True
            elif tx['to'] == '0x63ce21bd9af8cc603322cb025f26db567de8102b' and tx['methodId'] == '0xfb89f3b1':
                df.loc[wallet, 'yooldo_daily_task'] = True
            # Week 3
            elif tx['to'] == '0xd1a3abf42f9e66be86cfdea8c5c2c74f041c5e14' and tx['methodId'] == '0x5b7d7482':
                df.loc[wallet, 'send_mail'] = True
            elif tx['to'] == '0xe5d7c2a44ffddf6b295a15c148167daaaf5cf34f' and tx['methodId'] == '0xd0e30db0':
                df.loc[wallet, 'wrap_eth'] = True
            elif tx['to'] == '0xc043bce9af87004398181a8de46b26e63b29bf99' and tx['methodId'] == '0xefef39a1':
                df.loc[wallet, 'asmatch_mint'] = True
            elif tx['to'] == '0x37d4bfc8c583d297a0740d734b271eac9a88ade4' and tx['methodId'] == '0x183ff085':
                df.loc[wallet, 'bitavatar_checkin'] = True
            elif tx['to'] == '0x8286d601a0ed6cf75e067e0614f73a5b9f024151' and tx['methodId'] == '0x7859bb8d':
                df.loc[wallet, 'readon_curate'] = True
            elif tx['to'] == '0x2933749e45796d50eba9a352d29eed6fe58af8bb' and tx['methodId'] == '0xf02bc6d5':
                df.loc[wallet, 'sendingme_send'] = True
            # Week 4
            elif tx['to'] == '0x47874ff0bef601d180a8a653a912ebbe03739a1a' and tx['methodId'] == '0xefef39a1':
                df.loc[wallet, 'sarubol_mint'] = True
            elif tx['to'] == '0x490d76b1e9418a78b5403740bd70dfd4f6007e0f' and tx['methodId'] == '0x36ab86c4':
                df.loc[wallet, 'z2048_start_game'] = True
            elif tx['to'] == '0xc577018b3518cd7763d143d7699b280d6e50fdb6' and tx['methodId'] == '0x70245bdc':
                df.loc[wallet, 'lucky_cat_mint'] = True
            # Week 5
            elif tx['to'] == '0x7136abb0fa3d88e4b4d4ee58fc1dfb8506bb7de7' and tx['methodId'] == '0x1249c58b':
                df.loc[wallet, 'omnizone_mint'] = True
            elif tx['to'] == '0x578705c60609c9f02d8b7c1d83825e2f031e35aa' and tx['methodId'] == '0x6871ee40':
                df.loc[wallet, 'battlemon_mint'] = True
            elif tx['to'] == '0x9df3c2c75a92069b99c73bd386961631f143727c' and tx['methodId'] == '0x57bc3d78':
                df.loc[wallet, 'play_nouns'] = True

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

        cols = ['gamer_boom_proof', 'nidum_mint', 'townstory_mint', 'travelbag_mint', 'abuse_world_mint',
                'pictograph_mint', 'pictograph_stake', 'satoshi_universe_mint', 'yooldo_daily_task', 'send_mail',
                'wrap_eth', 'asmatch_mint', 'bitavatar_checkin', 'readon_curate', 'sendingme_send', 'sarubol_mint',
                'z2048_start_game', 'lucky_cat_mint', 'omnizone_mint', 'battlemon_mint', 'play_nouns']

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
                    self.parse_transactions(transactions['result'][:100], wallet_info['address'], df)
                else:
                    print(transactions)
            except:
                logger.warning(f'Can not parse {address} wallet')
        df.fillna(False).to_excel('progress.xlsx')
