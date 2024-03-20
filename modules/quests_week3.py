import random

from loguru import logger
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account
from config import ALIENSWAP_ABI, ASMATCH_CONTRACT, READON_CONTRACT, READON_ABI


class Week3(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="linea")

    @retry
    @check_gas
    async def asmatch_mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Start AsMatch mint")
        contract = self.get_contract(ASMATCH_CONTRACT, ALIENSWAP_ABI)

        balance = await contract.functions.balanceOf(self.address).call()
        if balance > 0:
            logger.warning(f"[{self.account_id}][{self.address}] AsMatch already minted. Skip module")
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
    async def bitavatar_checkin(self):
        logger.info(f"[{self.account_id}][{self.address}] Start BitAvatar check-in")
        contract = "0x37D4BFc8c583d297A0740D734B271eAc9a88aDe4"

        tx_data = await self.get_tx_data()
        tx_data['data'] = '0x183ff085'
        tx_data['to'] = self.w3.to_checksum_address(contract)

        signed_txn = await self.sign(tx_data)
        txn_hash = await self.send_raw_transaction(signed_txn)
        await self.wait_until_tx_finished(txn_hash.hex())

    @retry
    @check_gas
    async def readon_curate(self):
        logger.info(f"[{self.account_id}][{self.address}] Start ReadOn curate")
        contract = self.get_contract(READON_CONTRACT, READON_ABI)

        content_url = random.randint(1709924291302671616, 18446744073709551614)

        tx_data = await self.get_tx_data()
        transaction = await contract.functions.curate(
            content_url
        ).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)
        txn_hash = await self.send_raw_transaction(signed_txn)
        await self.wait_until_tx_finished(txn_hash.hex())

    @retry
    @check_gas
    async def sendingme_send(self, min_amount, max_amount, decimal):
        logger.info(f"[{self.account_id}][{self.address}] Start SendingMe task")
        contract = "0x2933749e45796d50eba9a352d29eed6fe58af8bb"

        data = "0xf02bc6d5" \
               "00000000000000000000000000000000000000000000000000005af3107a4000" \
               "000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"

        amount = round(random.uniform(min_amount, max_amount), decimal)
        amount_wei = self.w3.to_wei(amount, "ether")

        tx_data = await self.get_tx_data(amount_wei)
        tx_data['to'] = self.w3.to_checksum_address(contract)
        tx_data['data'] = data

        signed_txn = await self.sign(tx_data)
        txn_hash = await self.send_raw_transaction(signed_txn)
        await self.wait_until_tx_finished(txn_hash.hex())

