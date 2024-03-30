from loguru import logger
from utils.gas_checker import check_gas
from utils.helpers import retry, quest_checker
from .account import Account
from utils.nidim_sign import generate_claim_data
from utils.townstory_sign import get_townstory_signature, get_travelbag_signature
from config import NIDUM_CONTRACT, NIDUM_ABI,\
    TOWNSTORY_ABI, TOWNSTORY_CONTRACT,\
    TOWNSTORY_TRAVELBAG_ABI, TOWNSTORY_TRAVELBAG_CONTRACT


class Week1(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="linea")

    @quest_checker
    @retry
    @check_gas
    async def gamer_boom_mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Start Gamer Boom Mint OAT")
        contract = "0xc0b4ab5cb0fdd6f5dfddb2f7c10c4c6013f97bf2"

        tx_data = await self.get_tx_data()
        tx_data['data'] = '0x1249c58b'
        tx_data['to'] = self.w3.to_checksum_address(contract)

        signed_txn = await self.sign(tx_data)
        txn_hash = await self.send_raw_transaction(signed_txn)
        await self.wait_until_tx_finished(txn_hash.hex())

    @quest_checker
    @retry
    @check_gas
    async def gamer_boom_proof(self):

        logger.info(f"[{self.account_id}][{self.address}] Start Gamer Boom proof")
        contract = "0x6CD20be8914A9Be48f2a35E56354490B80522856"

        tx_data = await self.get_tx_data()
        tx_data['data'] = '0xb9a2092d'
        tx_data['to'] = self.w3.to_checksum_address(contract)

        signed_txn = await self.sign(tx_data)
        txn_hash = await self.send_raw_transaction(signed_txn)
        await self.wait_until_tx_finished(txn_hash.hex())

        return True

    @quest_checker
    @retry
    @check_gas
    async def nidum_mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Start nidum mint")

        contract = self.get_contract(NIDUM_CONTRACT, NIDUM_ABI)
        claim_data = await generate_claim_data(self.address, self.private_key, self.w3, self.proxy)
        message = claim_data['message']
        signature = claim_data['signature']

        tx_data = await self.get_tx_data()
        transaction = await contract.functions.mintFromShadowBatch(
            [9], [1], 0, message, signature
        ).build_transaction(tx_data)

        signed_tx = await self.sign(transaction)
        tnx_hash = await self.send_raw_transaction(signed_tx)
        await self.wait_until_tx_finished(tnx_hash.hex())

        return True

    @quest_checker
    @retry
    @check_gas
    async def nidum_bonus(self):
        logger.info(f"[{self.account_id}][{self.address}] Start nidum burn nft (bonus)")
        contract = self.get_contract(NIDUM_CONTRACT, NIDUM_ABI)
        token_id = 9

        balance = await contract.functions.balanceOf(self.address, token_id).call()
        if balance == 0:
            logger.error(f"[{self.account_id}][{self.address}] No nidum nft. Mint first. Skip module")
            return

        tx_data = await self.get_tx_data()
        transaction = await contract.functions.burn(
            self.address, 9, 1
        ).build_transaction(tx_data)

        signed_tx = await self.sign(transaction)
        tnx_hash = await self.send_raw_transaction(signed_tx)
        await self.wait_until_tx_finished(tnx_hash.hex())

        return True

    @quest_checker
    @retry
    @check_gas
    async def townstory_mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Start Townstory mint")

        contract = self.get_contract(TOWNSTORY_CONTRACT, TOWNSTORY_ABI)

        signature, deadline = get_townstory_signature(self.address, self.private_key, self.w3, self.proxy)

        tx_data = await self.get_tx_data()
        transaction = await contract.functions.createAccountSign(
                signature, 0, deadline
            ).build_transaction(tx_data)

        signed_tx = await self.sign(transaction)
        tnx_hash = await self.send_raw_transaction(signed_tx)
        await self.wait_until_tx_finished(tnx_hash.hex())

        return True

    @quest_checker
    @retry
    @check_gas
    async def travelbag_mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Start Townstory Travelbag mint")

        contract = self.get_contract(TOWNSTORY_TRAVELBAG_CONTRACT, TOWNSTORY_TRAVELBAG_ABI)
        signature, deadline = get_travelbag_signature(self.address, self.proxy)

        tx_data = await self.get_tx_data()
        transaction = await contract.functions.claimLineaTravelbag(
            signature, self.address, deadline
        ).build_transaction(tx_data)

        signed_tx = await self.sign(transaction)
        tnx_hash = await self.send_raw_transaction(signed_tx)
        await self.wait_until_tx_finished(tnx_hash.hex())

        return True
