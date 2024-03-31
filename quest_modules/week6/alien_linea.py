from config import ALIEN_LINEA_CONTRACT, ALIEN_LINEA_ABI
from ..account import Account
from typing import Union
from hashlib import sha256
from typing import Union
from loguru import logger
from utils.gas_checker import check_gas
from utils.helpers import retry


class AlienLinea(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)
        self.contract = self.get_contract(ALIEN_LINEA_CONTRACT, ALIEN_LINEA_ABI)

    @check_gas
    @retry
    async def mintNft(self):
        logger.info(f"[{self.account_id}][{self.address}] Минт Alien Linea")
        balance = await self.contract.functions.balanceOf(self.address).call()
        if (balance == 0):
            price = self.w3.to_wei(0.0001, 'ether')
            txData = await self.getTxData(value=price)
            tx = await self.contract.functions.purchase(1).build_transaction(txData)
            signedTx = await self.sign(tx)
            txHash = await self.send_raw_transaction(signedTx)
            await self.wait_until_tx_finished(txHash.hex())
        else:
            logger.info(f"[{self.account_id}][{self.address}] Alien Linea уже сминчена")