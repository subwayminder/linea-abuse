from config import ZACE_CONTRACT, ZACE_METHOD
from ..account import Account
from typing import Union
from hashlib import sha256
from typing import Union
from loguru import logger
from utils.gas_checker import check_gas
from utils.helpers import retry

class Zace(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)

    @check_gas
    @retry
    async def mintZace(self):
        logger.info(f"[{self.account_id}][{self.address}] Zace Mint")
        value = self.w3.to_wei(0.00005, 'ether')
        txData = await self.getTxData(value)
        txData['data'] = ZACE_METHOD
        txData['to'] = ZACE_CONTRACT
        signedTx = await self.sign(txData)
        txHash = await self.send_raw_transaction(signedTx)
        await self.wait_until_tx_finished(txHash.hex())