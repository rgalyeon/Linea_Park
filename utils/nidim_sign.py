from json import dumps
from aiohttp import ClientSession
from eth_account.messages import encode_defunct
import requests


async def register_wallet(wallet, proxy):
    url = f'https://auth.sidusheroes.com/api/v1/users'
    headers = {'Content-Type': 'application/json'}
    data = {'address': wallet.lower()}
    json_data = dumps(data)

    async with ClientSession() as session:
        async with session.post(url, headers=headers, data=json_data, proxy=proxy) as response:
            res = await response.json()
    return res


async def get_msg(wallet, proxy):
    url = 'https://auth.sidusheroes.com/api/v1/users/' + wallet.lower()

    async with ClientSession() as session:
        async with session.get(url, proxy=proxy) as response:
            res = await response.json()

    if res['message'] != 'success':
        raise ValueError('Bad response')
    nonce = res['data']['nonce']
    msg_text = f'Please sign this message to connect to sidusheroes.com: {nonce}'
    return msg_text


async def auth(wallet, signature, proxy):
    url = 'https://auth.sidusheroes.com/api/v1/auth'
    data = {"address": f"{wallet}", "signature": f"{signature}"}
    headers = {'Content-Type': 'application/json'}

    json_data = dumps(data)

    async with ClientSession() as session:
        async with session.post(url, headers=headers, data=json_data, proxy=proxy) as response:
            res = await response.json()

    if res['message'] != 'success':
        raise ValueError('Bad response')
    bearer = res['data']['accessToken']
    return bearer


async def get_token_data(wallet, bearer, proxy):
    url = f'https://plsrv.sidusheroes.com/shadow-game-linea/api/v1/item'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {bearer}'}
    data = {
        "user": f"{wallet.lower()}",
        "contract": "0x34Be5b8C30eE4fDe069DC878989686aBE9884470",
        "tokenId": 9
    }

    json_data = dumps(data)

    async with ClientSession() as session:
        async with session.post(url, headers=headers, data=json_data, proxy=proxy) as response:
            res = await response.json()
            # print(res)

    return res


def get_claim_data(wallet, bearer, proxies):
    url = 'https://plsrv.sidusheroes.com/shadow-game-linea/api/v1/claim'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {bearer}',
        'Origin': "https://play.sidusheroes.com",
        "Referer": "https://play.sidusheroes.com/",

        'Content-Length': '151',
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
    }

    data = {
        "contract": "0x34Be5b8C30eE4fDe069DC878989686aBE9884470",
        "user": f"{wallet.lower()}",
        "tokensData": [
            {
                "tokenId": 9,
                "amount": "1"
            }
        ]
    }

    json_data = dumps(data)

    res = requests.post(url, data=json_data, headers=headers, proxies=proxies)
    response = res.json()
    return response


def sign_message(private, message_text, w3):
    text_hex = "0x" + message_text.encode('utf-8').hex()
    text_encoded = encode_defunct(hexstr=text_hex)
    signed_message = w3.eth.account.sign_message(text_encoded, private_key=private)
    signature = signed_message.signature
    return signature.hex()


async def generate_claim_data(wallet, private, w3, proxy):
    proxies = {'http': proxy,
               'https': proxy}

    await register_wallet(wallet, proxy)
    msg_text = await get_msg(wallet, proxy)
    signature = sign_message(private, msg_text, w3)
    bearer = await auth(wallet, signature, proxy)
    await get_token_data(wallet, bearer, proxy)
    claim_data = get_claim_data(wallet, bearer, proxies)
    return claim_data
