from loguru import logger
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account
from config import (SATOSHI_UNIVERSE_CONTRACT, WIZARDS_ABI)


class CSZN_week2(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="linea")

    @retry
    @check_gas
    async def satoshi_universe_mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Start Satoshi Universe Mint")
        contract = self.get_contract(SATOSHI_UNIVERSE_CONTRACT, WIZARDS_ABI)

        n_nfts = await contract.functions.balanceOf(self.address).call()
        if n_nfts == 0:
            tx_data = await self.get_tx_data()
            transaction = await contract.functions.mintEfficientN2M_001Z5BWH().build_transaction(tx_data)

            signed_tx = await self.sign(transaction)
            tnx_hash = await self.send_raw_transaction(signed_tx)
            await self.wait_until_tx_finished(tnx_hash.hex())
        else:
            logger.info(f"[{self.account_id}][{self.address}] Already Minted")
