from config import TANUKI_CONTRACT, TANUKI_ABI
from ..account import Account
from typing import Union
from hashlib import sha256
from typing import Union
from loguru import logger
from utils.gas_checker import check_gas
from utils.helpers import retry

class TanukiNft(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)
        self.contract = self.get_contract(TANUKI_CONTRACT, TANUKI_ABI)

    @check_gas
    @retry
    async def mintNft(self):
        balance = await self.contract.functions.balanceOf(self.address).call()
        print(balance)
        if(balance == 0):
            txData = await self.getTxData(100000000000000)
            tx = await self.contract.functions.purchase(1).build_transaction(txData)
            signedTx = await self.sign(tx)
            txHash = await self.send_raw_transaction(signedTx)
            await self.wait_until_tx_finished(txHash.hex())
        else:
            logger.info("Tanuki NFT уже сминчена")