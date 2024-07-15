from loguru import logger
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account
from config import (ELEMENT_CONTRACT, ELEMENT_ABI, WIZARDS_ABI)


class CSZN_week3(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="linea")

    @retry
    @check_gas
    async def ascendtheend_mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Start Ascend The End Mint")
        launchpad_contract = self.get_contract(ELEMENT_CONTRACT, ELEMENT_ABI)
        nft_contract = self.get_contract('0xc83CCbd072B0CC3865dbD4BC6c3d686Bb0b85915', WIZARDS_ABI)

        n_nfts = await nft_contract.functions.balanceOf(self.address).call()
        if n_nfts == 0:
            tx_data = await self.get_tx_data()
            transaction = await launchpad_contract.functions.launchpadBuy(
                '0x0c21cfbb',
                '0x19a747c1',
                0,
                1,
                [],
                b''
            ).build_transaction(tx_data)

            signed_tx = await self.sign(transaction)
            tnx_hash = await self.send_raw_transaction(signed_tx)
            await self.wait_until_tx_finished(tnx_hash.hex())
        else:
            logger.info(f"[{self.account_id}][{self.address}] Already Minted")
