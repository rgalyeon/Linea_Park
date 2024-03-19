import json

import cryptography.fernet
from cryptography.fernet import Fernet
from getpass import getpass
import os
from pathlib import Path
import base64
from hashlib import md5
from typing import Dict
from config import ENCRYPTED_DATA_PATH, WALLET_DATA_PATH, SHEET_NAME
from settings import USE_PROXY
import pandas as pd
import numpy as np
from loguru import logger


def generate_key_from_password(password: str) -> bytes:
    md5_password = md5(password.encode()).hexdigest()
    return base64.urlsafe_b64encode(md5_password.encode())


def get_user_password(is_keys_encrypted: bool) -> bytes:
    """
    Simple interface for getting password from user input
    :param is_keys_encrypted: True if keys are encrypted
    :return: key
    """
    if is_keys_encrypted:
        password = getpass('Enter the password: ')
    else:
        while True:
            password = getpass('Create password: ')
            password_verif = getpass('Verify password: ')
            if password != password_verif:
                print('Verification failed')
                continue
            break
    return generate_key_from_password(password)


def load_wallet_data(password) -> Dict:

    # read wallet data
    encrypted_data_path = Path(ENCRYPTED_DATA_PATH)
    wallets_path = Path(WALLET_DATA_PATH)

    if not encrypted_data_path.exists():
        raise ValueError(f'File does not exist {encrypted_data_path}')
    if not wallets_path.exists():
        raise ValueError(f'File does not exist {wallets_path}')

    with open(encrypted_data_path, 'rb') as f:
        encoded_keys = f.read()

    wallets = pd.read_excel(wallets_path, sheet_name=SHEET_NAME)['address'].map(str.lower).tolist()

    fernet = Fernet(password)
    wallet_data = json.loads(fernet.decrypt(encoded_keys).decode())

    # check encrypted data
    missed_wallets = []
    curr_wallet_data = {}
    for wallet in wallets:
        if wallet not in wallet_data:
            missed_wallets.append(wallet)
        else:
            curr_wallet_data[wallet] = wallet_data[wallet]
    if missed_wallets:
        logger.warning(f'This wallets are not encrypted. Please, use encrypt module')
        print('\n'.join(missed_wallets))

    return curr_wallet_data


def handle_data(wallets_data_df: pd.DataFrame):

    wallet_names = wallets_data_df['name'].replace([np.nan], None)
    wallets = wallets_data_df['address'].map(str.lower)
    keys = wallets_data_df['private']
    proxies = wallets_data_df['proxy'].replace([np.nan], None)
    okx_apis = wallets_data_df['okx_api'].replace([np.nan], None)
    okx_addresses = wallets_data_df['okx_address'].replace([np.nan], None)

    if len(keys.dropna()) != len(wallets.dropna()):
        raise ValueError('Length of wallets != length of private keys')
    if USE_PROXY and len(proxies) != 0 and len(proxies.dropna()) != len(wallets.dropna()):
        logger.warning('Count of wallets != count of proxies')

    return wallet_names, wallets, keys, proxies, okx_apis, okx_addresses


def format_data(wallet_names, wallets, keys, proxies, okx_apis, okx_addresses):
    wallet_data = dict()
    for id_, (wallet, private_key, proxy, okx_api, name, okx_address) in enumerate(zip(wallets, keys, proxies,
                                                                                       okx_apis, wallet_names,
                                                                                       okx_addresses), start=1):
        okx_api_key, okx_secret, okx_password = None, None, None
        if okx_api:
            okx_api_key, okx_secret, okx_password = okx_api.split(';')
        wallet_data[wallet] = {
            'address': wallet,
            'id': name if name else id_,
            'private_key': private_key,
            'proxy': proxy,
            'okx_api': {
                'apiKey': okx_api_key,
                'secret': okx_secret,
                'password': okx_password,
                'proxy_url': ''
            },
            'okx_address': okx_address,
        }
    return wallet_data


def clean_and_save_data(wallets_data_df: pd.DataFrame):
    # clear data keys
    df_len = len(wallets_data_df)
    for col in ['private', 'proxy', 'okx_api', 'name', 'okx_address']:
        wallets_data_df[col] = [None] * df_len

    wallets_data_df.to_excel(WALLET_DATA_PATH, sheet_name='evm', index=False)


def encrypt_private_keys(password: bytes):
    wallets_path = Path(WALLET_DATA_PATH)

    if not wallets_path.exists():
        raise ValueError(f"File does not exist {wallets_path}")

    wallets_data_df = pd.read_excel(wallets_path, sheet_name=SHEET_NAME)
    wallet_names, wallets, keys, proxies, okx_apis, okx_addresses = handle_data(wallets_data_df)
    wallet_data = format_data(wallet_names, wallets, keys, proxies, okx_apis, okx_addresses)
    clean_and_save_data(wallets_data_df)

    fernet = Fernet(password)
    encrypted_data = fernet.encrypt(json.dumps(wallet_data).encode())
    with open(ENCRYPTED_DATA_PATH, 'wb') as f:
        f.write(encrypted_data)


def get_wallet_data() -> Dict:
    n_attempts = 3
    is_keys_encrypted = os.path.exists(ENCRYPTED_DATA_PATH)

    for _ in range(n_attempts):
        try:
            password = get_user_password(is_keys_encrypted)
            if not is_keys_encrypted:
                encrypt_private_keys(password)
            wallet_data = load_wallet_data(password)
            break
        except cryptography.fernet.InvalidToken:
            print('Wrong Password')
    else:
        raise ValueError('Wrong password')
    return wallet_data


if __name__ == '__main__':
    get_wallet_data()
