from config import UNFETTERED_EXPEDITION_NFT_CONTRACT, UNFETTERED_EXPEDITION_NFT_ABI
from ..account import Account
from typing import Union
from hashlib import sha256
from typing import Union
from loguru import logger
from utils.gas_checker import check_gas
from utils.helpers import retry


class UnfetteredExpeditionNft(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)
        self.contract = self.get_contract(UNFETTERED_EXPEDITION_NFT_CONTRACT, UNFETTERED_EXPEDITION_NFT_ABI)

    @check_gas
    @retry
    async def mintNft(self):
        logger.info(f"[{self.account_id}][{self.address}] Минт Unfettered expedition nft (Осторожно - нет проверки на владение)")
        txData = await self.getTxData()
        tx = await self.contract.functions.mint().build_transaction(txData)
        signedTx = await self.sign(tx)
        txHash = await self.send_raw_transaction(signedTx)
        await self.wait_until_tx_finished(txHash.hex())