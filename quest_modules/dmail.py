from config import DMAIL_ABI, DMAIL_CONTRACT
from .account import Account
from typing import Union
from hashlib import sha256
from typing import Union
from loguru import logger
import random
from utils.gas_checker import check_gas
from utils.helpers import retry


class Dmail(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)
        self.contract = self.get_contract(DMAIL_CONTRACT, DMAIL_ABI)
    @check_gas
    @retry
    async def sendMail(self):
        logger.info(f"[{self.account_id}][{self.address}] Отправка dmail")
        txData = await self.getTxData()
        email = sha256(str(1e11 * random.random()).encode()).hexdigest()
        theme = sha256(str(1e11 * random.random()).encode()).hexdigest()
        tx = await self.contract.functions.send_mail(email, theme).build_transaction(txData)
        signedTx = await self.sign(tx)
        txHash = await self.send_raw_transaction(signedTx)
        await self.wait_until_tx_finished(txHash.hex())