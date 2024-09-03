import pandas as pd
from tqdm import tqdm
import requests
import random
import time
from loguru import logger


class PohChecker:

    def __init__(self, wallets_data):
        self.wallets_data = wallets_data
        self.all_proxies = [wallet_info['proxy'] for wallet_info in self.wallets_data if wallet_info['proxy']]

        self.attest_names = {
            'clique': 'Clique',
            'dauth-openid3': 'Openid3',
            'gitcoin-passport': 'Gitcoin',
            'nomis': 'Nomis',
            'orange-protocol': 'Orange',
            'pado-labs': 'PADO',
            'ruby-score': 'RubyScore',
            'trusta-poh-attestation': 'Trusta POH',
            'trusta-reputation-attestation': 'Trusta Rep Score',
            'voyage-nft': 'Voyage NFT',
            'zk-pass-coinbase-kyc': 'Coinbase KYC',
            'zk-pass-okx-kyc': 'OKX KYC',
            'zk-pass-uber-trips': 'Uber',
            '0x-score': 'OxScore'
        }

    @staticmethod
    def get_poh_info(address, proxies=None):
        url = f'https://linea-xp-poh-api.linea.build/poh/{address}'
        if proxies:
            try:
                response = requests.get(url, proxies=proxies, timeout=10)
            except:
                response = requests.get(url)
        else:
            response = requests.get(url)
        res = response.json()
        return res

    def wait_poh(self, address):
        n_attemps = 10
        while n_attemps:
            proxy = random.choice(self.all_proxies)
            proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
            poh_info = self.get_poh_info(address.lower(), proxies)
            if poh_info:
                return poh_info
            n_attemps -= 1
            time.sleep(5)

    def parse_poh(self, wallet, poh_info, df):
        df.loc[wallet, :] = False
        df.loc[wallet, 'PoH'] = poh_info['poh']
        for attest in poh_info['attestations']:
            try:
                attest_name = self.attest_names[attest['issuerSlugName']]
            except KeyError:
                attest_name = attest['issuerSlugName']
            df.loc[wallet, attest_name] = attest['validated']

    def check_attest(self):
        logger.info('Start PoH check')

        cols = ['PoH', 'Gitcoin', 'PADO', 'Trusta POH', 'Voyage NFT', 'Coinbase KYC', 'OKX KYC', 'Uber', 'Clique',
                'Openid3', 'Nomis', 'Orange', 'RubyScore', 'Trusta Rep Score', '0xScore']

        df = pd.DataFrame(columns=cols)
        for wallet_info in tqdm(self.wallets_data):
            address = wallet_info['address'].lower()
            proxies = {'http': f'http://{wallet_info["proxy"]}', 'https': f'http://{wallet_info["proxy"]}'}
            try:
                poh_info = self.get_poh_info(address, proxies)
                if not poh_info:
                    poh_info = self.wait_poh(address)
            except:
                poh_info = self.wait_poh(address)
            try:
                if poh_info:
                    self.parse_poh(wallet_info['address'], poh_info, df)
                else:
                    logger.warning(f'Can not parse {address} wallet')
            except Exception as e:
                logger.warning(f'Can not parse {address} wallet. Error: {e}')
        df.fillna(False).to_excel('poh.xlsx')
