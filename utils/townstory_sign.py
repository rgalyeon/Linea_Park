from time import time
from json import dumps
import requests
from eth_account.messages import encode_defunct


def get_time_nonce():
    time_nonce = int(time() / 86400)
    return time_nonce


def get_address_line(address):
    address_line = (address[:19] + '...' + address[-18:]).lower()
    return address_line


def get_message(wallet):
    nonce = get_time_nonce()
    address_line = get_address_line(wallet)
    message = ('Welcome to Town Story! \n\n'
               'Click to sign in and accept the Town Story\n'
               'Terms of Service:\n'
               'https://townstory.io/\n\n'
               'This request will not trigger a blockchain\n'
               'transaction or cost any gas fees.\n\n'
               'Your authentication status will reset after\n'
               'each session.\n\n'
               'Wallet address:\n'
               f'{address_line}\n\n'
               f'Nonce: {nonce}')
    return message


def get_txn_signature(wallet, message_signature, proxies):

    data = {"header": {"version": "1.0.1", "baseVersion": "1.0.0", "referer": ""},
            "transaction": {"func": "register.loginByWallet",
                            "params": {"hall": 0, "wallet": "metamask", "chain": "linea",
                                       "signature": message_signature, "address": wallet.lower()}}}
    json_data = dumps(data)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = 'https://aws-login.townstory.io/town-login/handler.php'

    r = requests.post(url, data=json_data, headers=headers, proxies=proxies)
    res = r.json()
    if res['result'] != 'failed':
        txn_signature = res['response']['signature']
        deadline = res['response']['deadline']
        return txn_signature, deadline


def sign_message(private, message_text, w3):
    text_hex = "0x" + message_text.encode('utf-8').hex()
    text_encoded = encode_defunct(hexstr=text_hex)
    signed_message = w3.eth.account.sign_message(text_encoded, private_key=private)
    signature = signed_message.signature
    return signature.hex()


def get_townstory_signature(wallet, private, w3, proxy):
    proxies = {'http': proxy,
               'https': proxy}

    message_text = get_message(wallet)
    message_signature = sign_message(private, message_text, w3)
    signature, deadline = get_txn_signature(wallet, message_signature, proxies)
    return signature, deadline


def get_travelbag_signature(wallet, proxy):
    proxies = {'http': proxy,
               'https': proxy}
    url = 'https://townstory.io//api'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        "Content-Length": "70",
        "Accept": "*/*",
        "Origin": "https://townstory.io",
        "Referer": "https://townstory.io/linea"

    }
    data = {"action": "getLineaSign", "address": f'{wallet.lower()}'}

    r = requests.post(url, data=data, headers=headers, proxies=proxies)
    res = r.json()
    return res['signature'], res['deadline']
