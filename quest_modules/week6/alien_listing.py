import eth_abi
from config import ALIEN_LISTING_CONTRACT, ALIEN_LISTING_ABI
from ..account import Account
from typing import Union
from loguru import logger
from random import choice
from utils.gas_checker import check_gas
from utils.helpers import retry

class AlienListing(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)
        self.contract = self.get_contract(ALIEN_LISTING_CONTRACT, ALIEN_LISTING_ABI)

    @check_gas
    @retry
    async def runListing(self):
        logger.info(f"[{self.account_id}][{self.address}] Alien Listing")
        txData = await self.getTxData()
        tx = await self.contract.functions.setApprovalForAll('0x7E0E8675DACEC5ADbc5d27EB278d8aE5D84d01F9', True).build_transaction(txData)
        signedTx = await self.sign(tx)
        txHash = await self.send_raw_transaction(signedTx)
        await self.wait_until_tx_finished(txHash.hex())