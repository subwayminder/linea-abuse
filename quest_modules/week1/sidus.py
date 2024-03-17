from config import SIDUS_CONTRACT, SIDUS_ABI
from ..account import Account
from typing import Union
from hashlib import sha256
from typing import Union
from loguru import logger
from utils.gas_checker import check_gas
from utils.helpers import retry
from eth_account.messages import encode_defunct
import requests


class SidusMint(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)
        self.contract = self.get_contract(SIDUS_CONTRACT, SIDUS_ABI)
    
    
    def getAccessToken(self):
        sidusAuth = requests.get("https://auth.sidusheroes.com/api/v1/users/" + self.address)
        if(sidusAuth.status_code == 404):
            sidusAuth = requests.post("https://auth.sidusheroes.com/api/v1/users/", json={
                "address": self.address
            })
        sidusAuth = sidusAuth.json()
        nonce = str(sidusAuth['data']['nonce'])
        message = encode_defunct(text='Please sign this message to connect to sidusheroes.com: ' + nonce)
        sign = self.w3.eth.account.sign_message(message, private_key=self.private_key).signature
        authData = {
            "address": self.address,
            "signature": sign.hex()
        }
        return requests.post('https://auth.sidusheroes.com/api/v1/auth', authData).json()['data']['accessToken']

    def getClaimData(self):
        accessToken = self.getAccessToken()

        claimPayload = {
            "contract": SIDUS_CONTRACT,
            "user": self.address,
            "tokensData": [
                {
                    "tokenId": 9,
                    "amount": "1"
                }
            ]
        }

        return requests.post(url='https://plsrv.sidusheroes.com/shadow-game-linea/api/v1/claim', 
                                    json = claimPayload, 
                                    headers = {"Authorization": "Bearer " + accessToken}
                                )

    @check_gas
    @retry
    async def mintNft(self):
        logger.info(f"[{self.account_id}][{self.address}] МинтSidus")
        claimPayload = self.getClaimData()
        if (claimPayload.status_code == 400):
            logger.info(f"[{self.account_id}][{self.address}] МинтSidus сейчас недоступен")
        else:
            balance = await self.contract.functions.balanceOf(self.address, 9).call()
            if (balance == 0):
                claimPayload = claimPayload.json()
                message = claimPayload['message']
                sign = claimPayload['signature']
                nonce = claimPayload['nonce']
                txData = await self.getTxData()
                tx = await self.contract.functions.mintFromShadowBatch([9], [1], int(nonce), message, sign).build_transaction(txData)
                signedTx = await self.sign(tx)
                txHash = await self.send_raw_transaction(signedTx)
                await self.wait_until_tx_finished(txHash.hex())
            else:
                logger.info(f"[{self.account_id}][{self.address}] МинтSidus - NFT уже сминчена")

    async def releaseNft(self):
            balance = await self.contract.functions.balanceOf(self.address, 9).call()
            if (balance != 0):
                txData = await self.getTxData()
                tx = await self.contract.functions.burn(self.address, 9, 1).build_transaction(txData)
                signedTx = await self.sign(tx)
                txHash = await self.send_raw_transaction(signedTx)
                await self.wait_until_tx_finished(txHash.hex())
            else:
                logger.info(f"[{self.account_id}][{self.address}] МинтSidus - NFT еще не сминчена")