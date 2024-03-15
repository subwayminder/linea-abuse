from config import GAMIC_CONTRACT, GAMIC_ABI
from .account import Account
from typing import Union
from hashlib import sha256
from typing import Union
from loguru import logger
from web3 import Web3
from utils.gas_checker import check_gas
from utils.helpers import retry


class Gamic(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)
        self.contract = self.get_contract(GAMIC_CONTRACT, GAMIC_ABI)
    @check_gas
    @retry
    async def depositWeth(self):
        amount_wei, amount, balance = await self.getAmount(
            "ETH",
            0.000001,
            0.000002,
            18,
            False,
            60,
            80
        )
        txData = await self.getTxData(value=amount_wei)
        tx = await self.contract.functions.deposit().build_transaction(txData)
        signedTx = await self.sign(tx)
        txHash = await self.send_raw_transaction(signedTx)
        await self.wait_until_tx_finished(txHash.hex())