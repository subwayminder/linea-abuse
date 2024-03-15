from config import BITAVATAR_ABI, BITAVATAR_CONTRACT
from .account import Account
from typing import Union


class BitAvatar(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)
        self.contract = self.get_contract(BITAVATAR_CONTRACT, BITAVATAR_ABI)

    async def checkIn(self):
        txData = await self.getTxData()
        tx = await self.contract.functions.checkIn().build_transaction(txData)
        signedTx = await self.sign(tx)
        txHash = await self.send_raw_transaction(signedTx)
        await self.wait_until_tx_finished(txHash.hex())