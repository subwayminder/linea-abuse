from config import YOOLDOO_CONTRACT, YOOLDOO_ABI
from ..account import Account
from typing import Union
from hashlib import sha256
from typing import Union
from loguru import logger
from utils.gas_checker import check_gas
from utils.helpers import retry

# TODO: не работает, допилить по возможности
class Yooldoo(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)
        self.contract = self.get_contract(YOOLDOO_CONTRACT, YOOLDOO_ABI)

    @check_gas
    @retry
    async def run(self):
        txData = await self.getTxData(value=2000000000000)
        tx = await self.contract.functions.standUp('0xfb89f3b1').build_transaction(txData)
        signedTx = await self.sign(tx)
        txHash = await self.send_raw_transaction(signedTx)
        await self.wait_until_tx_finished(txHash.hex())