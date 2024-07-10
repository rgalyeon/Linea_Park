from loguru import logger
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account
from config import (SATOSHI_UNIVERSE_CONTRACT, WIZARDS_ABI,
                    ELEMENT_CONTRACT, ELEMENT_ABI)


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

    @retry
    @check_gas
    async def linus_mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Start Linus Eggs Mint")
        launchpad_contract = self.get_contract(ELEMENT_CONTRACT, ELEMENT_ABI)
        nft_contract = self.get_contract('0xfca530bC063C2e1Eb1d399a7A43F8991544B57Bf', WIZARDS_ABI)

        n_nfts = await nft_contract.functions.balanceOf(self.address).call()
        if n_nfts == 0:
            tx_data = await self.get_tx_data()
            transaction = await launchpad_contract.functions.launchpadBuy(
                '0x0c21cfbb',
                '0x1ffca9db',
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

    @retry
    @check_gas
    async def yooldo_mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Start Yooldo mint")

        contract = "0xF502AA456C4ACe0D77d55Ad86436F84b088486F1"
        nft_contract = self.get_contract(contract, WIZARDS_ABI)

        n_nfts = await nft_contract.functions.balanceOf(self.address).call()
        if n_nfts == 0:
            tx_data = await self.get_tx_data()

            tx_data['to'] = self.w3.to_checksum_address(contract)
            tx_data['data'] = '0x1249c58b'

            signed_txn = await self.sign(tx_data)
            txn_hash = await self.send_raw_transaction(signed_txn)
            await self.wait_until_tx_finished(txn_hash.hex())
        else:
            logger.info(f"[{self.account_id}][{self.address}] Already Minted")
