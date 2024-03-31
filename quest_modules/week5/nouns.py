import eth_abi
from config import NOUNS_CONTRACT, NOUNS_CURRENCY, NOUNS_ABI
from ..account import Account
from typing import Union
from loguru import logger
from random import choice
from utils.gas_checker import check_gas
from utils.helpers import retry

class Nouns(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)
        self.contract = self.get_contract(NOUNS_CONTRACT, NOUNS_ABI)

    @check_gas
    @retry
    async def claim(self):
        logger.info(f"[{self.account_id}][{self.address}] Nouns")
        txData = await self.getTxData()
        tx = await self.contract.functions.claim(
            self.address, 
            0, 
            1, 
            NOUNS_CURRENCY, 
            0,
            [
                [eth_abi.encode(['bytes32'], [b''])], 
                2 ** 256 - 1, 
                0, 
                NOUNS_CURRENCY
            ], 
            b''
        ).build_transaction(txData)
        signedTx = await self.sign(tx)
        txHash = await self.send_raw_transaction(signedTx)
        await self.wait_until_tx_finished(txHash.hex())