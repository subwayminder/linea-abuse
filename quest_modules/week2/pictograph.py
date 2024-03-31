from config import PICTOGRAPHS_ABI, PICTOGRAPHS_CONTRACT
from ..account import Account
from typing import Union
from hashlib import sha256
from typing import Union
from loguru import logger
from utils.gas_checker import check_gas
from utils.helpers import retry


class Pictograph(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)
        self.contract = self.get_contract(PICTOGRAPHS_CONTRACT, PICTOGRAPHS_ABI)

    @check_gas
    @retry
    async def mintNft(self):
        logger.info(f"[{self.account_id}][{self.address}] Минт Pictograph")
        balance = await self.contract.functions.balanceOf(self.address).call()
        if (balance == 0):
            price = await self.contract.functions.price().call()
            txData = await self.getTxData(value=price)
            tx = await self.contract.functions.mintNFT().build_transaction(txData)
            signedTx = await self.sign(tx)
            txHash = await self.send_raw_transaction(signedTx)
            await self.wait_until_tx_finished(txHash.hex())
        else:
            logger.info(f"[{self.account_id}][{self.address}] Pictogram NFT уже сминчена")

    @check_gas
    @retry
    async def stake(self):
        logger.info(f"[{self.account_id}][{self.address}] Стейкаем Pictograph")
        nft_id = await self.contract.functions.tokenOfOwnerByIndex(self.address, 0).call()
        txData = await self.getTxData()
        tx = await self.contract.functions.stake(nft_id).build_transaction(txData)
        signedTx = await self.sign(tx)
        txHash = await self.send_raw_transaction(signedTx)
        await self.wait_until_tx_finished(txHash.hex())