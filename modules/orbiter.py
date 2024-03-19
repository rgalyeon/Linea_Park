import aiohttp
from loguru import logger

from utils.helpers import retry
from config import ORBITER_MAKER
from .transfer import Transfer


class Orbiter(Transfer):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info)

        self.chain_ids = {
            "ethereum": "1",
            "arbitrum": "42161",
            "optimism": "10",
            "zksync": "324",
            "nova": "42170",
            "zkevm": "1101",
            "scroll": "534352",
            "base": "8453",
            "linea": "59144",
            "zora": "7777777",
        }

        self.orbiter_ids = {
            'ethereum': '1',
            'optimism': '7',
            'bsc': '15',
            'arbitrum': '2',
            'nova': '16',
            'polygon': '6',
            'polygon_zkevm': '17',
            'zksync': '14',
            'zksync_lite': '3',
            'starknet': '4',
            'linea': '23',
            'base': '21',
            'mantle': '24',
            'scroll': '19',
            'zora': '30',
        }

    @retry
    async def get_bridge_amount(self, from_chain: str, to_chain: str, amount: float):
        url = "https://openapi.orbiter.finance/explore/v3/yj6toqvwh1177e1sexfy0u1pxx5j8o47"

        data = {
            "id": 1,
            "jsonrpc": "2.0",
            "method": "orbiter_calculatedAmount",
            "params": [f"{self.chain_ids[from_chain]}-{self.chain_ids[to_chain]}:ETH-ETH", float(amount)]
        }

        async with aiohttp.ClientSession() as session:
            response = await session.post(
                url=url,
                headers={"Content-Type": "application/json"},
                json=data,
            )

            response_data = await response.json()

            if response_data.get("result").get("error", None) is None:
                return int(response_data.get("result").get("_sendValue"))

            else:
                error_data = response_data.get("result").get("error")

                logger.error(f"[{self.account_id}][{self.address}] Orbiter error | {error_data}")

                return False

    async def bridge_logic(self, source_chain, destination_chain, amount_wei, amount, balance):
        from_chain_id = self.orbiter_ids[self.chain]
        to_chain_id = self.orbiter_ids[destination_chain]
        maker_x_maker = f'{from_chain_id}-{to_chain_id}'

        contract = ORBITER_MAKER[maker_x_maker]['ETH-ETH']['makerAddress']

        logger.info(
            f"[{self.account_id}][{self.address}] Bridge {self.chain} –> {destination_chain} | {amount} ETH"
        )

        bridge_amount = await self.get_bridge_amount(self.chain, destination_chain, amount)

        if bridge_amount is False:
            return

        balance = await self.w3.eth.get_balance(self.w3.to_checksum_address(self.address))

        if bridge_amount > balance:
            logger.error(f"[{self.account_id}][{self.address}] Insufficient funds!")
            raise ValueError('Insufficient funds!')
        else:
            tx_data = await self.get_tx_data(bridge_amount)
            tx_data.update({"to": self.w3.to_checksum_address(contract)})

            signed_txn = await self.sign(tx_data)

            txn_hash = await self.send_raw_transaction(signed_txn)

            await self.wait_until_tx_finished(txn_hash.hex())
