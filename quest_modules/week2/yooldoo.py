from config import YOOLDOO_CONTRACT, YOOLDOO_ABI, YOOLDOO_METHOD_ID
from ..account import Account
from typing import Union
from hashlib import sha256
from typing import Union
from loguru import logger
from utils.gas_checker import check_gas
from utils.helpers import retry

class Yooldoo(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)
        self.contract = self.get_contract(YOOLDOO_CONTRACT, YOOLDOO_ABI)

    @check_gas
    @retry
    async def runStandUp(self):
        logger.info(f"[{self.account_id}][{self.address}] Yooldoo stand up")
        value = self.w3.to_wei(0.0001, 'ether')
        txData = await self.getTxData(value)
        txData['data'] = YOOLDOO_METHOD_ID
        txData['to'] = YOOLDOO_CONTRACT
        signedTx = await self.sign(txData)
        txHash = await self.send_raw_transaction(signedTx)
        await self.wait_until_tx_finished(txHash.hex())