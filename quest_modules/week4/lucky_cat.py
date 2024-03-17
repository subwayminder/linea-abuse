from config import LUCKY_CAT_CONTRACT, LUCKY_CAT_ABI
from ..account import Account
from typing import Union
from hashlib import sha256
from typing import Union
from loguru import logger
from utils.gas_checker import check_gas
from utils.helpers import retry

class LuckyCat(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)
        self.contract = self.get_contract(LUCKY_CAT_CONTRACT, LUCKY_CAT_ABI)

    @check_gas
    @retry
    async def adoptCat(self):
        logger.info(f"[{self.account_id}][{self.address}] Adopt Lucky Cat")
        txData = await self.getTxData()
        tx = await self.contract.functions.adoptCat().build_transaction(txData)
        signedTx = await self.sign(tx)
        txHash = await self.send_raw_transaction(signedTx)
        await self.wait_until_tx_finished(txHash.hex())