from loguru import logger
from utils.gas_checker import check_gas
from utils.helpers import retry, quest_checker
from .account import Account
from config import (MICRO3_ABI, MICRO3_CONTRACT,
                    ALIENSWAP_ABI, ALIENSWAP_CONTRACT,
                    FROG_WAR_CONTRACT, FROG_WAR_ABI, WARRIOR_CONTRACT,
                    BILINEAR_CONTRACT, BILINEAR_ABI,
                    IMAGINEAI_CONTRACT, IMAGINEAI_ABI,
                    ARENAGAMES_CONTRACT, ARENAGAMES_ABI
                    )
from eth_abi import encode
from web3 import Web3


class Week6(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="linea")

    @quest_checker
    @retry
    @check_gas
    async def zace_check_in(self):
        logger.info(f"[{self.account_id}][{self.address}] Start zAce check in")
        contract = '0x971a871fd8811abbb1f5e3fb1d84a873d381cee4'

        amount = self.w3.to_wei(0.00005, 'ether')
        tx_data = await self.get_tx_data(amount)
        tx_data['data'] = '0xbaeb0718'
        tx_data['to'] = self.w3.to_checksum_address(contract)

        signed_txn = await self.sign(tx_data)
        txn_hash = await self.send_raw_transaction(signed_txn)
        await self.wait_until_tx_finished(txn_hash.hex())

        return True

    @quest_checker
    @retry
    @check_gas
    async def micro3_mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Start Micro3 mint")
        contract = self.get_contract(MICRO3_CONTRACT, MICRO3_ABI)

        balance = await contract.functions.balanceOf(self.address).call()
        if balance > 0:
            logger.warning(f"[{self.account_id}][{self.address}] Micro3 already minted. Skip module")
            return

        tx_data = await self.get_tx_data()
        transaction = await contract.functions.purchase(0).build_transaction(tx_data)

        signed_tx = await self.sign(transaction)
        tnx_hash = await self.send_raw_transaction(signed_tx)
        await self.wait_until_tx_finished(tnx_hash.hex())

        return True

    @quest_checker
    @retry
    @check_gas
    async def alienswap_mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Start Alienswap mint")
        contract = self.get_contract(ALIENSWAP_CONTRACT, ALIENSWAP_ABI)

        balance = await contract.functions.balanceOf(self.address).call()
        if balance > 0:
            logger.warning(f"[{self.account_id}][{self.address}] Alienswap already minted. Skip module")
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

        return True

    # @quest_checker
    # @retry
    # @check_gas
    # async def alienswap_bonus(self):
    #     """
    #     Doesn't work on Layer3
    #     """
    #     logger.info(f"[{self.account_id}][{self.address}] Start Alienswap bonus task")
    #     contract = self.get_contract(ALIENSWAP_CONTRACT, ALIENSWAP_ABI)
    #     list_contract = self.w3.to_checksum_address('0x7e0e8675dacec5adbc5d27eb278d8ae5d84d01f9')
    #
    #     tx_data = await self.get_tx_data()
    #     transaction = await contract.functions.setApprovalForAll(list_contract, True).build_transaction(tx_data)
    #     signed_tx = await self.sign(transaction)
    #     tnx_hash = await self.send_raw_transaction(signed_tx)
    #     await self.wait_until_tx_finished(tnx_hash.hex())
    #
    #     return True

    @quest_checker
    @retry
    @check_gas
    async def frog_war_mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Start Frog War mint")
        contract = self.get_contract(FROG_WAR_CONTRACT, FROG_WAR_ABI)

        _receiver = self.address
        _tokenId = 1
        _quantity = 1
        _currency = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'
        _pricePerToken = 100000000000000

        amount = self.w3.to_wei(0.0001, "ether")
        tx_data = await self.get_tx_data(amount)
        transaction = await contract.functions.claim(
            _receiver, _tokenId, _quantity, _currency, _pricePerToken,
            [[encode(['bytes32'], [b''])], 1, _pricePerToken, _currency], b''
        ).build_transaction(tx_data)
        signed_tx = await self.sign(transaction)
        tnx_hash = await self.send_raw_transaction(signed_tx)
        await self.wait_until_tx_finished(tnx_hash.hex())

        return True

    @quest_checker
    @retry
    @check_gas
    async def frog_war_bonus(self):
        logger.info(f"[{self.account_id}][{self.address}] Start Frog War Bonus mint")
        contract = self.get_contract(WARRIOR_CONTRACT, FROG_WAR_ABI)

        _receiver = self.address
        _tokenId = 6
        _quantity = 1
        _currency = '0x21d624c846725ABe1e1e7d662E9fB274999009Aa'
        _pricePerToken = 0

        tx_data = await self.get_tx_data()
        transaction = await contract.functions.claim(
            _receiver, _tokenId, _quantity, _currency, _pricePerToken,
            [[encode(['bytes32'], [b''])], 1, _pricePerToken, _currency], b''
        ).build_transaction(tx_data)
        signed_tx = await self.sign(transaction)
        tnx_hash = await self.send_raw_transaction(signed_tx)
        await self.wait_until_tx_finished(tnx_hash.hex())

        return True

    @quest_checker
    @retry
    @check_gas
    async def acg_worlds_mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Start ACGWORLDS mint")
        contract = '0xcd1ea9e70d0260c0f47d217ed6d5be9cd4ed34fb'

        amount = self.w3.to_wei(0.0001, "ether")
        tx_data = await self.get_tx_data(amount)
        tx_data['data'] = '0x1249c58b'
        tx_data['to'] = self.w3.to_checksum_address(contract)

        signed_txn = await self.sign(tx_data)
        txn_hash = await self.send_raw_transaction(signed_txn)
        await self.wait_until_tx_finished(txn_hash.hex())

        return True

    @quest_checker
    @retry
    @check_gas
    async def bilinear_mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Start Bilinear mint")
        contract = self.get_contract(BILINEAR_CONTRACT, BILINEAR_ABI)

        tx_data = await self.get_tx_data()
        transaction = await contract.functions.claim(
            [],
            ([], [1]),
            ([], [], []),
            0,
            Web3.to_bytes(hexstr="9ce46a75af5117679e3393d8844ec85ed684cf325e48be9822469e12cfe53482")
        ).build_transaction(tx_data)
        signed_tx = await self.sign(transaction)
        tnx_hash = await self.send_raw_transaction(signed_tx)
        await self.wait_until_tx_finished(tnx_hash.hex())

        return True

    @quest_checker
    @retry
    @check_gas
    async def imagineairynfts_mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Start ImagineAIryNFTs mint")
        contract = self.get_contract(IMAGINEAI_CONTRACT, IMAGINEAI_ABI)
        uri = "https://ipfs.io/ipfs/bafyreidwx4uav5zivvk7kto2pwszxlcqazqpbxub24zbkk5xzmeiugdap4/metadata.json"

        amount = self.w3.to_wei(0.0001, "ether")
        tx_data = await self.get_tx_data(amount)
        transaction = await contract.functions.mint(uri).build_transaction(tx_data)

        signed_tx = await self.sign(transaction)
        tnx_hash = await self.send_raw_transaction(signed_tx)
        await self.wait_until_tx_finished(tnx_hash.hex())

        return True

    @quest_checker
    @retry
    @check_gas
    async def arenagames_mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Start Arena Games mint")
        contract = self.get_contract(ARENAGAMES_CONTRACT, ARENAGAMES_ABI)

        tx_data = await self.get_tx_data()
        transaction = await contract.functions.safeMint(self.address).build_transaction(tx_data)

        signed_tx = await self.sign(transaction)
        tnx_hash = await self.send_raw_transaction(signed_tx)
        await self.wait_until_tx_finished(tnx_hash.hex())

        return True
