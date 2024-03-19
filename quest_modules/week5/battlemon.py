from config import BATTLEMON_NFT_CONTRACT, BATTLEMON_NFT_ABI
from ..account import Account
from typing import Union
from hashlib import sha256
from typing import Union
from loguru import logger
from utils.gas_checker import check_gas
from utils.helpers import retry


class BattlemonNft(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)
        self.contract = self.get_contract(BATTLEMON_NFT_CONTRACT, BATTLEMON_NFT_ABI)

    @check_gas
    @retry
    async def mintNft(self):
        logger.info(f"[{self.account_id}][{self.address}] Минт Battlemon NFT")
        balance = await self.contract.functions.balanceOf(self.address).call()
        if(balance == 0):
            txData = await self.getTxData()
            tx = await self.contract.functions.safeMint().build_transaction(txData)
            signedTx = await self.sign(tx)
            txHash = await self.send_raw_transaction(signedTx)
            await self.wait_until_tx_finished(txHash.hex())
        else:
            logger.info(f"[{self.account_id}][{self.address}] Battlemon NFT уже есть")