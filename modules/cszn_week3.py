from loguru import logger
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account
from config import (ELEMENT_CONTRACT, ELEMENT_ABI, WIZARDS_ABI,
                    DEMMORTAL_CONTRACT, DEMMORTAL_ABI)


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

    @retry
    @check_gas
    async def sendingme_mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Start Sending Me mint")

        contract = "0xEaea2Fa0dea2D1191a584CFBB227220822E29086"
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

    @retry
    @check_gas
    async def townstory_mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Start Townstory mint")
        contract = self.get_contract("0x8Ad15e54D37d7d35fCbD62c0f9dE4420e54Df403", WIZARDS_ABI)

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
    async def danielle_zosavac_mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Start Danielle Zosavac mint")
        contract = self.get_contract("0x3A21e152aC78f3055aA6b23693FB842dEFdE0213", WIZARDS_ABI)

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
    async def demmortal_mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Start Demmortal mint")
        contract = self.get_contract(DEMMORTAL_CONTRACT, DEMMORTAL_ABI)

        id_ = 0
        amount = 1

        n_nfts = await contract.functions.balanceOf(self.address, id_).call()
        if n_nfts == 0:
            tx_data = await self.get_tx_data()
            transaction = await contract.functions.mint(
                self.address,
                id_,
                amount,
                b''
            ).build_transaction(tx_data)

            signed_tx = await self.sign(transaction)
            tnx_hash = await self.send_raw_transaction(signed_tx)
            await self.wait_until_tx_finished(tnx_hash.hex())
        else:
            logger.info(f"[{self.account_id}][{self.address}] Already Minted")
