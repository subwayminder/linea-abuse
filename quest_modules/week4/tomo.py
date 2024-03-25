from config import TOMO_CONTRACT, TOMO_ABI
from ..account import Account
from typing import Union
from hashlib import sha256
from typing import Union
from loguru import logger
from utils.gas_checker import check_gas
from utils.helpers import retry

# TODO: Допилить по возможности
class TomoNft(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)
        self.contract = self.get_contract(TOMO_CONTRACT, TOMO_ABI)

    @check_gas
    @retry
    async def mintNft(self):
        print(self.address)
        buyPrice = await self.contract.functions.getBuyPrice('0x000000000000000000000000000000000078406c696b686f6e5f796f756e7573', 1).call()
        print(buyPrice)
        txData = await self.getTxData(buyPrice)
        tx = await self.contract.functions.buyVotePass(bytes('0x000000000000000000000000000000000078406c696b686f6e5f796f756e7573', 'utf-8'), 1, 27, bytes('0xfb88b5c6d653cd92a11286adddc6ece0b8eccfe5810829ffec5ee647f273491e', 'utf-8'), bytes('0x2445b2ed26a46fa37ebda3797061e00f621c7e86babd80c1bba62fb9fea69578', 'utf-8')).build_transaction(txData)
        signedTx = await self.sign(tx)
        txHash = await self.send_raw_transaction(signedTx)
        await self.wait_until_tx_finished(txHash.hex())