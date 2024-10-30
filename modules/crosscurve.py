import json

import aiohttp
from .transfer import Transfer
from loguru import logger
from config import RPC, CROSSCURVE_ABI

class CrossCurve(Transfer):
    def __init__(self, wallet_info):
        super().__init__(wallet_info=wallet_info)

    async def get_routing_params(self, from_chain_id, to_chain_id, amount_wei):
        data = {
            "params": {
                "chainIdIn": from_chain_id,
                "chainIdOut": to_chain_id,
                "tokenIn": "0x0000000000000000000000000000000000000000",
                "tokenOut": "0x0000000000000000000000000000000000000000",
                "amountIn": f"{amount_wei}"
            },
            "slippage": 1
        }

        async with aiohttp.ClientSession() as session:
            response = await session.post(
                url='https://api.crosscurve.fi/routing/scan',
                headers={"Content-Type": "application/json"},
                json=data,
            )

            try:
                response_data = await response.json()
            except Exception as e:
                logger.error(f"[{self.account_id}][{self.address}] Bad response | {e}")
                return

        return response_data

    async def estimate_route(self, route):

        async with aiohttp.ClientSession() as session:
            response = await session.post(
                url='https://api.crosscurve.fi/estimate',
                headers={"Content-Type": "application/json"},
                json=route,
            )

            try:
                response_data = await response.json()
            except Exception as e:
                logger.error(f"[{self.account_id}][{self.address}] Bad response | {e}")
                return

        return response_data

    async def forming_data_for_tx(self, routing, estimate):

        data = {
            "from": self.address,
            "recipient": self.address,
            "routing": routing[0],
            "estimate": estimate
        }

        async with aiohttp.ClientSession() as session:
            response = await session.post(
                url='https://api.crosscurve.fi/tx/create',
                headers={"Content-Type": "application/json"},
                json=data,
            )

            try:
                response_data = await response.json()
            except Exception as e:
                logger.error(f"[{self.account_id}][{self.address}] Bad response | {e}")
                return
        return response_data


    async def bridge_logic(self, source_chain, destination_chain, amount_wei, amount, balance):
        logger.info(f'[{self.account_id}][{self.address}] Start transfer {amount} ETH from {source_chain} to {destination_chain}')

        from_chain_id = RPC[source_chain]['chain_id']
        to_chain_id = RPC[destination_chain]['chain_id']

        routing_data = await self.get_routing_params(from_chain_id, to_chain_id, amount_wei)
        estimate = await self.estimate_route(routing_data[0])

        raw_tx = await self.forming_data_for_tx(routing_data, estimate)
        contract = self.get_contract(raw_tx['to'], CROSSCURVE_ABI)

        tx_data = await self.get_tx_data(value=int(raw_tx['value']) + int(estimate['executionPrice']))
        transaction = await contract.functions.start(
            raw_tx['args'][0],
            raw_tx['args'][1],
            [
                int(raw_tx['args'][2]['executionPrice']),
                int(raw_tx['args'][2]['deadline']),
                int(raw_tx['args'][2]['v']),
                raw_tx['args'][2]['r'],
                raw_tx['args'][2]['s']
            ]
        ).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)
        txn_hash = await self.send_raw_transaction(signed_txn)
        await self.wait_until_tx_finished(txn_hash.hex())