from loguru import logger
from config import LAYERBANK_CONTRACT, LAYERBANK_WETH_CONTRACT, LAYERBANK_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from utils.sleeping import sleep
from .account import Account


class LayerBank(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="linea")

        self.contract = self.get_contract(LAYERBANK_CONTRACT, LAYERBANK_ABI)

    async def router(self, min_amount,
                     max_amount,
                     decimal,
                     sleep_from,
                     sleep_to,
                     make_withdraw,
                     all_amount,
                     min_percent,
                     max_percent,
                     required_amount_for_withdraw):

        amount_wei, amount, balance = await self.get_amount(
            "ETH",
            min_amount,
            max_amount,
            decimal,
            all_amount,
            min_percent,
            max_percent
        )

        await self.deposit(amount_wei, amount, balance)
        if make_withdraw:
            await sleep(sleep_from, sleep_to)
            await self.withdraw(required_amount_for_withdraw)

    async def get_deposit_amount(self):
        weth_contract = self.get_contract(LAYERBANK_WETH_CONTRACT)

        amount = await weth_contract.functions.balanceOf(self.address).call()

        return amount

    @retry
    @check_gas
    async def deposit(self, amount_wei, amount, balance) -> None:

        logger.info(f"[{self.account_id}][{self.address}] Make deposit on LayerBank | {amount} ETH")

        tx_data = await self.get_tx_data(amount_wei)

        transaction = await self.contract.functions.supply(
            self.w3.to_checksum_address(LAYERBANK_WETH_CONTRACT),
            amount_wei,
        ).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())

    @retry
    @check_gas
    async def withdraw(self, required_amount_for_withdraw) -> None:
        amount = await self.get_deposit_amount()
        balance = self.w3.from_wei(amount, 'ether')

        if amount > 0 and balance >= required_amount_for_withdraw:
            logger.info(
                f"[{self.account_id}][{self.address}] Make withdraw from LayerBank | " +
                f"{balance} ETH"
            )

            await self.approve(amount, LAYERBANK_WETH_CONTRACT, LAYERBANK_CONTRACT)

            tx_data = await self.get_tx_data()

            transaction = await self.contract.functions.redeemUnderlying(
                self.w3.to_checksum_address(LAYERBANK_WETH_CONTRACT),
                amount,
            ).build_transaction(tx_data)

            signed_txn = await self.sign(transaction)

            txn_hash = await self.send_raw_transaction(signed_txn)

            await self.wait_until_tx_finished(txn_hash.hex())
        else:
            logger.error(f"[{self.account_id}][{self.address}] Deposit not found or no deposit with required amount")
