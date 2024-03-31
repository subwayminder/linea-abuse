from config import IMAGINALRY_CONTRACT, IMAGINALRY_ABI, IMAGINALRY_NFT_LINK
from ..account import Account
from typing import Union
from hashlib import sha256
from typing import Union
from loguru import logger
from utils.gas_checker import check_gas
from utils.helpers import retry


class Imaginalry(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)
        self.contract = self.get_contract(IMAGINALRY_CONTRACT, IMAGINALRY_ABI)

    @check_gas
    @retry
    async def mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Минт Imaginalry")
        balance = await self.contract.functions.balanceOf(self.address).call()
        if (balance == 0):
            price = self.w3.to_wei(0.00005, 'ether')
            txData = await self.getTxData(value=price)
            tx = await self.contract.functions.mint(IMAGINALRY_NFT_LINK).build_transaction(txData)
            signedTx = await self.sign(tx)
            txHash = await self.send_raw_transaction(signedTx)
            await self.wait_until_tx_finished(txHash.hex())
        else:
            logger.info(f"[{self.account_id}][{self.address}] Imaginalry уже сминчена")