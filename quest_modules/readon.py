from config import READON_ABI, READON_CONTRACT
from .account import Account
from typing import Union
from hashlib import sha256
from typing import Union
from loguru import logger
import random
import uuid
from utils.gas_checker import check_gas
from utils.helpers import retry


class ReadOn(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)
        self.contract = self.get_contract(READON_CONTRACT, READON_ABI)
    @check_gas
    @retry
    async def curate(self):
        logger.info(f"[{self.account_id}][{self.address}] Курирование на ReadOn")
        txData = await self.getTxData()
        url = uuid.uuid1().int>>64
        tx = await self.contract.functions.curate(url).build_transaction(txData)
        signedTx = await self.sign(tx)
        txHash = await self.send_raw_transaction(signedTx)
        await self.wait_until_tx_finished(txHash.hex())
