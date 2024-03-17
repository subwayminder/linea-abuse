from config import TOWN_STORY_NFT_CONTRACT, TOWN_STORY_NFT_ABI
from ..account import Account
from typing import Union
from hashlib import sha256
from typing import Union
from loguru import logger
from utils.gas_checker import check_gas
from utils.helpers import retry
import requests


class TownStoryNft(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)
        self.contract = self.get_contract(TOWN_STORY_NFT_CONTRACT, TOWN_STORY_NFT_ABI)

    def getMintData(self):
        data = requests.post(url='https://townstory.io//api', data={
            'action': 'getLineaSign',
            'address': self.address
        })
        if data.status_code == 200:
            sign = data.json()['signature']
            deadline = data.json()['deadline']
            return sign, deadline
        else:
            return None, None

    @check_gas
    @retry
    async def mintNft(self):
        logger.info(f"[{self.account_id}][{self.address}] Минт Town Story (BONUS)")
        balance = await self.contract.functions.getMintedAmount(self.address).call()
        if(balance == 0):
            sign, deadline = self.getMintData()
            if sign != None:
                txData = await self.getTxData()
                tx = await self.contract.functions.claimLineaTravelbag(sign, self.address, deadline).build_transaction(txData)
                signedTx = await self.sign(tx)
                txHash = await self.send_raw_transaction(signedTx)
                await self.wait_until_tx_finished(txHash.hex())
            else:
                logger.error(f"[{self.account_id}][{self.address}] Минт Town Story (BONUS) - ошибка авторизации")
        else:
            logger.info(f"[{self.account_id}][{self.address}] Town Story NFT уже есть")