import asyncio
import aiohttp
import traceback

from . import Account
from config import CHAINS_OKX
from loguru import logger
import random

import ccxt.async_support as ccxt_async
import math
import re
from utils.helpers import retry, sleep
import datetime
import base64
import hmac
from typing import List, Dict
from ccxt.base.errors import InsufficientFunds


class Okx(Account):

    def __init__(self, wallet_info: Dict, chains: List) -> None:
        super().__init__(wallet_info=wallet_info, chain=random.choice(chains))
        self.api_info = wallet_info['okx_api']

    async def get_data(self, request_path="/api/v5/account/balance?ccy=USDT", body='', meth="GET"):

        def signature(timestamp: str, method: str, request_path: str, secret_key: str, body: str = "") -> str:
            if not body:
                body = ""

            message = timestamp + method.upper() + request_path + body
            mac = hmac.new(
                bytes(secret_key, encoding="utf-8"),
                bytes(message, encoding="utf-8"),
                digestmod="sha256",
            )
            d = mac.digest()
            return base64.b64encode(d).decode("utf-8")

        dt_now = datetime.datetime.utcnow()
        ms = str(dt_now.microsecond).zfill(6)[:3]
        timestamp = f"{dt_now:%Y-%m-%dT%H:%M:%S}.{ms}Z"

        headers = {
            "Content-Type": "application/json",
            "OK-ACCESS-KEY": self.api_info['apiKey'],
            "OK-ACCESS-SIGN": signature(timestamp, meth, request_path, self.api_info['secret'], body),
            "OK-ACCESS-TIMESTAMP": timestamp,
            "OK-ACCESS-PASSPHRASE": self.api_info['password'],
            'x-simulated-trading': '0'
        }

        return headers

    @staticmethod
    async def make_http_request(url, method="GET", headers=None, params=None, data=None, timeout=10):
        async with aiohttp.ClientSession() as session:
            kwargs = {"url": url, "method": method, "timeout": timeout}

            if headers:
                kwargs["headers"] = headers
            if params:
                kwargs["params"] = params
            if data:
                kwargs["data"] = data

            async with session.request(**kwargs) as response:
                return await response.json()

    async def transfer_from_subaccounts(self, token_name):

        try:
            headers = await self.get_data(request_path="/api/v5/users/subaccount/list", meth="GET")
            list_sub = await self.make_http_request("https://www.okx.cab/api/v5/users/subaccount/list", headers=headers)

            for sub_data in list_sub['data']:
                name_sub = sub_data['subAcct']

                headers = await self.get_data(
                    request_path=f"/api/v5/asset/subaccount/balances?subAcct={name_sub}&ccy={token_name}", meth="GET")
                sub_balance = await self.make_http_request(
                    f"https://www.okx.cab/api/v5/asset/subaccount/balances?subAcct={name_sub}&ccy={token_name}",
                    headers=headers)
                sub_balance = sub_balance['data'][0]['bal']
                if float(sub_balance):
                    logger.info(f'Transfer {sub_balance} {token_name} from {name_sub} to main account')
                    body = {"ccy": f"{token_name}", "amt": str(sub_balance), "from": 6, "to": 6, "type": "2",
                            "subAcct": name_sub}
                    headers = await self.get_data(request_path=f"/api/v5/asset/transfer", body=str(body), meth="POST")
                    await self.make_http_request("https://www.okx.cab/api/v5/asset/transfer", data=str(body),
                                                 method="POST", headers=headers)
                await asyncio.sleep(1)

        except Exception as error:
            logger.error(f'Transfer from sub to main error {error}')
            raise ValueError

    async def transfer_spot_to_funding(self, token_name):

        headers = await self.get_data(request_path=f"/api/v5/account/balance?ccy={token_name}")
        balance = await self.make_http_request(f'https://www.okx.cab/api/v5/account/balance?ccy={token_name}',
                                               headers=headers)
        if balance["code"] == "0" and balance["data"][0]["details"]:
            balance = balance["data"][0]["details"][0]["cashBal"]

            if balance != 0:
                logger.info(f'Transfer {balance} {token_name} from spot to funding')
                body = {"ccy": f"{token_name}", "amt": float(balance), "from": 18, "to": 6, "type": "0", "subAcct": "",
                        "clientId": "", "loanTrans": "", "omitPosRisk": ""}
                headers = await self.get_data(request_path=f"/api/v5/asset/transfer", body=str(body), meth="POST")
                await self.make_http_request("https://www.okx.cab/api/v5/asset/transfer", data=str(body),
                                             method="POST", headers=headers)

    async def get_ccxt(self):
        exchange_config = self.api_info
        exchange_options = {
            'apiKey': exchange_config['apiKey'],
            'secret': exchange_config['secret'],
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot',
            }
        }

        if 'password' in exchange_config:
            exchange_options['password'] = exchange_config['password']

        if exchange_config.get('proxy_url'):
            exchange_options['proxies'] = {
                'http': exchange_config['proxy_url'],
                'https': exchange_config['proxy_url'],
            }

        exchange_class = getattr(ccxt_async, "okx")
        exchange = exchange_class(exchange_options)

        return exchange

    @staticmethod
    def smart_round(number):
        if isinstance(number, (int, float)):
            abs_num = abs(number)
            if abs_num == 0:
                return 0
            elif abs_num >= 1:
                return round(number, 2)
            elif 0 < abs_num < 1e-4:
                return "{:.8f}".format(number)
            else:
                return round(number, 3 - int(math.floor(math.log10(abs_num)) + 1))
        else:
            raise ValueError("    Функция принимает только числа (целые и с плавающей точкой) [function smart_round]")

    async def okx_get_withdrawal_info(self, exchange, token):
        currencies = await exchange.fetch_currencies()

        networks = []
        network_data = {}

        if currencies is not None:
            for currency_code, currency in currencies.items():
                if currency_code == token.upper():
                    networks_info = currency.get('networks')
                    if networks_info is not None:
                        for network, network_info in networks_info.items():

                            fee = network_info.get('fee')
                            if fee is not None:
                                fee = float(fee)
                                fee = self.smart_round(fee)

                            min_withdrawal = network_info.get('limits', {}).get('withdraw', {}).get('min')
                            if min_withdrawal is not None:
                                min_withdrawal = float(min_withdrawal)

                            id = network_info.get('id')
                            is_withdraw_enabled = network_info.get('withdraw', False)

                            if is_withdraw_enabled:
                                network_data[network] = (id, fee, min_withdrawal)
                                networks.append(network)
                    else:
                        raise ValueError(f"Currency {currency_code} doesn't contain 'networks' attribute")
        else:
            raise ValueError("Currencies not found")

        return networks, network_data

    @retry
    async def okx_withdraw(self, min_amount, max_amount, token_name,
                           terminate, skip_enabled, skip_threshold,
                           wait_unlimited_time, sleep_between_attempts: List[int]):
        network = CHAINS_OKX[self.chain]
        amount = round(random.uniform(min_amount, max_amount), 8)

        logger.info(f'[{self.account_id}][{self.address}] Start withdrawal from OKX {amount} {token_name} '
                    f'to {self.chain.capitalize()}')
        curr_balance_wei = await self.w3.eth.get_balance(self.address)

        curr_balance = curr_balance_wei / 10 ** 18
        if skip_enabled and curr_balance >= skip_threshold:
            logger.info(f'[{self.account_id}][{self.address}] Skip module! Wallet balance {curr_balance} {token_name}')
            return

        # await self.transfer_spot_to_funding(token_name)

        exchange = await self.get_ccxt()
        networks, networks_data = await self.okx_get_withdrawal_info(exchange, token_name)

        if network not in networks:
            raise ValueError(f'Cannot withdraw token {token_name} to {network} chain')
        okx_network_name, fee, min_withdrawal = networks_data[network]
        pattern = "^[^-]*-"
        network_name = re.sub(pattern, "", okx_network_name)
        while True:
            try:
                await self.transfer_from_subaccounts(token_name)
                await exchange.withdraw(token_name, amount, self.address,
                                        params={
                                            "chainName": okx_network_name,
                                            "fee": fee,
                                            "pwd": '-',
                                            "amt": self.smart_round(amount),
                                            "network": network_name,
                                        })
                break
            except InsufficientFunds:
                if wait_unlimited_time:
                    logger.info(f'[{self.account_id}][{self.address}] Waiting money on OKX')
                    await sleep(*sleep_between_attempts)
                else:
                    break
            except Exception as e:
                logger.error(f'Error {e} in withdrawal. Try to change min amount.')
                traceback.print_exc()
                if terminate:
                    await exchange.close()
                    exit()
                break

        await exchange.close()
        logger.info(f'Transaction sent. Waiting money from OKX')
        while curr_balance_wei == await self.w3.eth.get_balance(self.address):
            await asyncio.sleep(60)

        logger.success(f'[{self.account_id}][{self.address}] Successfully withdrawn {amount} {token_name} ')
        return True
