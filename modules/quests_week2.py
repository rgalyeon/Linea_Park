from loguru import logger
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account
from config import ABUSE_WORLD_CONTRACT, ALIENSWAP_ABI,\
    PICTOGRAPHS_CONTRACT, PICTOGRAPHS_ABI,\
    OMNISEA_CONTRACT, OMNISEA_ABI


class Week2(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="linea")

    @retry
    @check_gas
    async def abuse_world_mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Start Abuse World mint")
        contract = self.get_contract(ABUSE_WORLD_CONTRACT, ALIENSWAP_ABI)

        balance = await contract.functions.balanceOf(self.address).call()
        if balance > 0:
            logger.warning(f"[{self.account_id}][{self.address}] Abuse World already minted. Skip module")
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

    @retry
    @check_gas
    async def pictograph_mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Start Pictographs mint")

        contract = self.get_contract(PICTOGRAPHS_CONTRACT, PICTOGRAPHS_ABI)

        balance = await contract.functions.balanceOf(self.address).call()
        if balance > 0:
            logger.warning(f"[{self.account_id}][{self.address}] Pictographs already minted. Skip module")
            return

        tx_data = await self.get_tx_data()
        transaction = await contract.functions.mintNFT().build_transaction(tx_data)
        signed_tx = await self.sign(transaction)
        tnx_hash = await self.send_raw_transaction(signed_tx)

        await self.wait_until_tx_finished(tnx_hash.hex())

    @retry
    @check_gas
    async def pictograph_stake(self):
        """
        TODO NEED TEST
        """
        logger.info(f"[{self.account_id}][{self.address}] Start Pictographs stake")

        contract = self.get_contract(PICTOGRAPHS_CONTRACT, PICTOGRAPHS_ABI)
        balance = await contract.functions.balanceOf(self.address).call()
        if balance == 0:
            logger.error(f"[{self.account_id}][{self.address}] Not found NFT. Skip module")
            return

        token_id = await contract.functions.tokenOfOwnerByIndex(self.address, 0).call()

        tx_data = await self.get_tx_data()

        transaction = await contract.functions.stake(token_id).build_transaction(tx_data)

        signed_tx = await self.sign(transaction)
        tnx_hash = await self.send_raw_transaction(signed_tx)
        await self.wait_until_tx_finished(tnx_hash.hex())

    @retry
    @check_gas
    async def satoshi_universe_mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Start Satoshi Universe mint")

        contract = self.get_contract(OMNISEA_CONTRACT, OMNISEA_ABI)
        nft_address = "0x0dE240B2A3634fCD72919eB591A7207bDdef03cd"

        value = await contract.functions.fixedFee().call()

        tx_data = await self.get_tx_data(value=value)

        transaction = await contract.functions.mint(
            [self.address, nft_address, 1, [], 1, b'']
        ).build_transaction(tx_data)

        signed_tx = await self.sign(transaction)
        tnx_hash = await self.send_raw_transaction(signed_tx)
        await self.wait_until_tx_finished(tnx_hash.hex())

    @retry
    @check_gas
    async def yooldo_daily_task(self):
        logger.info(f"[{self.account_id}][{self.address}] Start Yooldo daily task")

        contract = "0x63ce21BD9af8CC603322cB025f26db567dE8102b"
        amount = self.w3.to_wei(0.0001, "ether")
        tx_data = await self.get_tx_data(value=amount)

        tx_data['to'] = self.w3.to_checksum_address(contract)
        tx_data['data'] = '0xfb89f3b1'

        signed_txn = await self.sign(tx_data)
        txn_hash = await self.send_raw_transaction(signed_txn)
        await self.wait_until_tx_finished(txn_hash.hex())

