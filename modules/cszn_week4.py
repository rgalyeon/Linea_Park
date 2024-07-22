import asyncio

import aiohttp
from loguru import logger
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account
from config import (COOPRECORDS_CONTRACT, COOPRECORDS_ABI)
from fake_useragent import UserAgent
import json


class CSZN_week4(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="linea")

    @retry
    @check_gas
    async def cooprecords_mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Start Coop Records Mint")
        contract = self.get_contract(COOPRECORDS_CONTRACT, COOPRECORDS_ABI)

        id_ = 1

        n_nfts = await contract.functions.balanceOf(self.address, id_).call()
        if n_nfts == 0:

            ua = UserAgent().getRandom
            link = 'https://public-api.phosphor.xyz/v1/purchase-intents'
            headers = {
                'accept': '*/*',
                'accept-language': 'uk',
                'content-type': 'application/json',
                'origin': 'https://app.phosphor.xyz',
                'priority': 'u=1, i',
                'referer': 'https://app.phosphor.xyz/',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': ua["os"],
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                "user-agent": ua['useragent']
            }

            data = {
                "buyer":  {"eth_address": self.address},
                "listing_id": "fceb2be9-f9fd-458a-8952-9a0a6f873aff",
                "provider": "MINT_VOUCHER",
                "quantity": "1"}

            timeout = aiohttp.ClientTimeout(total=2)
            while True:
                try:
                    async with aiohttp.ClientSession() as session:

                        async with session.post(link, data=json.dumps(data),
                                                headers=headers,
                                                proxy=self.proxy,
                                                timeout=timeout) as response:
                            if response.status in [200, 201]:
                                response_data = await response.json()
                                break
                        await asyncio.sleep(0.4)
                except aiohttp.ClientOSError as e:
                    logger.warning(f"[{self.account_id}][{self.address}] Connection Reset error. Retry")
                except asyncio.TimeoutError as e:
                    pass

            voucher = response_data['data']['voucher']
            signature = response_data['data']['signature']
            tx_data = await self.get_tx_data()
            transaction = await contract.functions.mintWithVoucher(
                [
                    voucher['net_recipient'],
                    voucher['initial_recipient'],
                    int(voucher['initial_recipient_amount']),
                    int(voucher['quantity']),
                    int(voucher['nonce']),
                    int(voucher['expiry']),
                    int(voucher['price']),
                    int(voucher['token_id']),
                    voucher['currency']
                ],
                signature
            ).build_transaction(tx_data)

            signed_tx = await self.sign(transaction)
            tnx_hash = await self.send_raw_transaction(signed_tx)
            await self.wait_until_tx_finished(tnx_hash.hex())
        else:
            logger.info(f"[{self.account_id}][{self.address}] Already Minted")
