import random

from loguru import logger
from utils.gas_checker import check_gas
from utils.helpers import retry, quest_checker
from .account import Account
from config import (OCTOMOS_CONTRACT, OCTOMOS_ABI,
                    CRAZYGANG_CONTRACT, CRAZYGANG_ABI,
                    MINTPAD_CONTRACT, MINTPAD_ABI,
                    WIZARDS_CONTRACT, WIZARDS_ABI)


class CSZN_week1(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="linea")

    @retry
    @check_gas
    async def octomos_mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Start OctoMos Mint")
        contract = self.get_contract(OCTOMOS_CONTRACT, OCTOMOS_ABI)
        nft_contract = self.get_contract("0xaa7f152D6e6dbD095c66Fd985B9bC88548A52350", OCTOMOS_ABI)

        launchpadId = '0x53b93973'
        slotId = 0
        quantity = 1

        n_nfts = await nft_contract.functions.balanceOf(self.address).call()
        if n_nfts == 0:
            tx_data = await self.get_tx_data()
            transaction = await contract.functions.launchpadBuy(
                '0x0c21cfbb',
                launchpadId,
                slotId,
                quantity,
                [],
                b""
            ).build_transaction(tx_data)

            signed_tx = await self.sign(transaction)
            tnx_hash = await self.send_raw_transaction(signed_tx)
            await self.wait_until_tx_finished(tnx_hash.hex())
        else:
            logger.info(f"[{self.account_id}][{self.address}] Already Minted")

    @retry
    @check_gas
    async def clutchai_mint(self, urls):
        logger.info(f"[{self.account_id}][{self.address}] Start Crazy Gang Mint")
        contract = self.get_contract(CRAZYGANG_CONTRACT, CRAZYGANG_ABI)

        link = random.choice(urls)

        n_nfts = await contract.functions.balanceOf(self.address).call()
        if n_nfts == 0:
            tx_data = await self.get_tx_data(value=self.w3.to_wei(0.00012, 'ether'))
            transaction = await contract.functions.safeMint(
                self.address,
                link
            ).build_transaction(tx_data)

            signed_tx = await self.sign(transaction)
            tnx_hash = await self.send_raw_transaction(signed_tx)
            await self.wait_until_tx_finished(tnx_hash.hex())
        else:
            logger.info(f"[{self.account_id}][{self.address}] Already Minted")

    @retry
    @check_gas
    async def mintpad_mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Start Push Mint")
        contract = self.get_contract(MINTPAD_CONTRACT, MINTPAD_ABI)

        _tokenId = 0
        _quantity = 1
        _currency = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
        _pricePerToken = 0
        _limitPerWallet = 2

        n_nfts = await contract.functions.balanceOf(self.address, _tokenId).call()
        if n_nfts == 0:
            tx_data = await self.get_tx_data(value=self.w3.to_wei(0.0000029, 'ether'))
            transaction = await contract.functions.claim(
                self.address,
                _tokenId,
                _quantity,
                _currency,
                _pricePerToken,
                [
                 [b'\x00' * 32],
                 _limitPerWallet,
                 _pricePerToken,
                 _currency],
                b""
            ).build_transaction(tx_data)

            signed_tx = await self.sign(transaction)
            tnx_hash = await self.send_raw_transaction(signed_tx)
            await self.wait_until_tx_finished(tnx_hash.hex())
        else:
            logger.info(f"[{self.account_id}][{self.address}] Already Minted")

    @retry
    @check_gas
    async def wizards_mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Start Wizards Mint")
        contract = self.get_contract(WIZARDS_CONTRACT, WIZARDS_ABI)

        n_nfts = await contract.functions.balanceOf(self.address).call()
        if n_nfts == 0:
            tx_data = await self.get_tx_data()
            transaction = await contract.functions.mintEfficientN2M_001Z5BWH().build_transaction(tx_data)

            signed_tx = await self.sign(transaction)
            tnx_hash = await self.send_raw_transaction(signed_tx)
            await self.wait_until_tx_finished(tnx_hash.hex())
        else:
            logger.info(f"[{self.account_id}][{self.address}] Already Minted")
