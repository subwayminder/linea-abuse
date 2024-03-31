from ..account import Account
from typing import Union
from hashlib import sha256
from typing import Union
from loguru import logger
from hexbytes import HexBytes
from utils.gas_checker import check_gas
from utils.helpers import retry
from config import SATOSHI_FAKE_WALLET
from random import randrange

class SatoshiTx(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)

    @check_gas
    @retry
    async def fakeTx(self):
        logger.info(f"[{self.account_id}][{self.address}] Satoshi")
        tx = {
            "chainId": await self.w3.eth.chain_id,
            "from": self.address,
            "to": SATOSHI_FAKE_WALLET,
            "value": randrange(5000000000000, 15000000000000),
            "gasPrice": await self.w3.eth.gas_price,
            "nonce": await self.w3.eth.get_transaction_count(self.address),
        }
        signedTx = await self.sign(tx)
        txHash = await self.send_raw_transaction(signedTx)
        await self.wait_until_tx_finished(txHash.hex())