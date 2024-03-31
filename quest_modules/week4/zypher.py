import eth_abi
from config import ZYPHER_CONTRACT, ZYPHER_METHOD_ID
from ..account import Account
from typing import Union
from loguru import logger
from random import choice
from utils.gas_checker import check_gas
from utils.helpers import retry

class Zypher(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)

    @check_gas
    @retry
    async def runTx(self):
        logger.info(f"[{self.account_id}][{self.address}] Zypher 2048")
        symbols = '0123456789abcdef'
        data_line = ''.join([choice(symbols) for _ in range(64)])
        txData = await self.getTxData()
        txData['data'] = ZYPHER_METHOD_ID + data_line + eth_abi.encode(['uint256'], [1]).hex()
        txData['to'] = ZYPHER_CONTRACT
        signedTx = await self.sign(txData)
        txHash = await self.send_raw_transaction(signedTx)
        await self.wait_until_tx_finished(txHash.hex())