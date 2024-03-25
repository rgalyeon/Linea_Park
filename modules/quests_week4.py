import random

from loguru import logger
from utils.gas_checker import check_gas
from utils.helpers import retry, quest_checker
from .account import Account
from config import ALIENSWAP_ABI, SARUBOL_CONTRACT, ZYPHER_CONTRACT, LUCKY_CAT_ABI, LUCKY_CAT_CONTRACT


class Week4(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="linea")

    @quest_checker
    @retry
    @check_gas
    async def sarubol_mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Start Sarubol mint")
        contract = self.get_contract(SARUBOL_CONTRACT, ALIENSWAP_ABI)

        balance = await contract.functions.balanceOf(self.address).call()
        if balance > 0:
            logger.warning(f"[{self.account_id}][{self.address}] Sarubol already minted. Skip module")
            return

        amount = self.w3.to_wei(0.0001, "ether")
        quantity = 1

        tx_data = await self.get_tx_data(value=amount)
        transaction = await contract.functions.purchase(
            quantity
        ).build_transaction(tx_data)

        signed_tx = await self.sign(transaction)
        tnx_hash = await self.send_raw_transaction(signed_tx)
        await self.wait_until_tx_finished(tnx_hash.hex())

        return True

    @quest_checker
    @retry
    @check_gas
    async def z2048_start_game(self):
        logger.info(f"[{self.account_id}][{self.address}] Start z2048 game")
        data = "0x36ab86c4"
        data += ''.join([random.choice('0123456789abcdef') for _ in range(64)])
        data += '0000000000000000000000000000000000000000000000000000000000000001'

        tx_data = await self.get_tx_data()
        tx_data['data'] = data
        tx_data['to'] = self.w3.to_checksum_address(ZYPHER_CONTRACT)

        signed_tx = await self.sign(tx_data)
        tnx_hash = await self.send_raw_transaction(signed_tx)
        await self.wait_until_tx_finished(tnx_hash.hex())

        return True

    @quest_checker
    @retry
    @check_gas
    async def lucky_cat_mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Start adopt cat")

        contract = self.get_contract(LUCKY_CAT_CONTRACT, LUCKY_CAT_ABI)

        tx_data = await self.get_tx_data()
        transaction = await contract.functions.adoptCat().build_transaction(tx_data)

        signed_tx = await self.sign(transaction)
        tnx_hash = await self.send_raw_transaction(signed_tx)
        await self.wait_until_tx_finished(tnx_hash.hex())

        return True
