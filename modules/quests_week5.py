import random

from loguru import logger
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account
from config import ALIENSWAP_ABI, OMNIZONE_CONTRACT, BATTLEMON_CONTRACT, UNFETTERED_CONTRACT


class Week5(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="linea")

    @retry
    @check_gas
    async def omnizone_mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Start Omnizone mint")
        contract = self.get_contract(OMNIZONE_CONTRACT, ALIENSWAP_ABI)

        balance = await contract.functions.balanceOf(self.address).call()
        if balance > 0:
            logger.warning(f"[{self.account_id}][{self.address}] Omnizone already minted. Skip module")
            return

        tx_data = await self.get_tx_data()
        tx_data['data'] = '0x1249c58b'
        tx_data['to'] = self.w3.to_checksum_address(OMNIZONE_CONTRACT)

        signed_txn = await self.sign(tx_data)
        txn_hash = await self.send_raw_transaction(signed_txn)
        await self.wait_until_tx_finished(txn_hash.hex())

    @retry
    @check_gas
    async def battlemon_mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Start Battlemon mint")
        contract = self.get_contract(BATTLEMON_CONTRACT, ALIENSWAP_ABI)

        balance = await contract.functions.balanceOf(self.address).call()
        if balance > 0:
            logger.warning(f"[{self.account_id}][{self.address}] Omnizone already minted. Skip module")
            return

        tx_data = await self.get_tx_data()
        tx_data['data'] = '0x6871ee40'
        tx_data['to'] = self.w3.to_checksum_address(BATTLEMON_CONTRACT)

        signed_tx = await self.sign(tx_data)
        tnx_hash = await self.send_raw_transaction(signed_tx)
        await self.wait_until_tx_finished(tnx_hash.hex())
