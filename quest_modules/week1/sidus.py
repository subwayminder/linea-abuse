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
        self.proxy = proxy
    
    def registerWallet(self):
        url = f'https://auth.sidusheroes.com/api/v1/users'
        headers = {'Content-Type': 'application/json'}
        data = {'address': self.address.lower(), "proxy": f"http://{self.proxy}"}
        requests.post(url=url, json=data, headers=headers)

    def getTokenData(self):
        accessToken = self.getAccessToken()
        url = f'https://plsrv.sidusheroes.com/shadow-game-linea/api/v1/item'
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {accessToken}', "proxy": f"http://{self.proxy}"}
        data = {"user": f"{self.address.lower()}", "contract": "0x34Be5b8C30eE4fDe069DC878989686aBE9884470", "tokenId": 9}
        requests.post(url=url, json=data, headers=headers)
    
    def getAccessToken(self):
        sidusAuth = requests.get(url="https://auth.sidusheroes.com/api/v1/users/" + self.address, headers={"proxy": f"http://{self.proxy}"})
        if(sidusAuth.status_code == 404):
            sidusAuth = requests.post(url="https://auth.sidusheroes.com/api/v1/users/", json={
                "address": self.address,
            },
            headers={"proxy": f"http://{self.proxy}"}
        )
        sidusAuth = sidusAuth.json()
        nonce = str(sidusAuth['data']['nonce'])
        message = encode_defunct(text='Please sign this message to connect to sidusheroes.com: ' + nonce)
        sign = self.w3.eth.account.sign_message(message, private_key=self.private_key).signature
        authData = {"address": self.address,"signature": sign.hex()}
        return requests.post(url='https://auth.sidusheroes.com/api/v1/auth', data=authData, headers={"proxy": f"http://{self.proxy}"}).json()['data']['accessToken']

    def getClaimData(self):
        accessToken = self.getAccessToken()

        claimPayload = {
            "contract": SIDUS_CONTRACT,
            "user": self.address.lower(),
            "tokensData": [
                {
                    "tokenId": 9,
                    "amount": "1"
                }
            ]
        }

        return requests.post(url='https://plsrv.sidusheroes.com/shadow-game-linea/api/v1/claim', 
                                    json = claimPayload, 
                                    headers = {
                                        "Authorization": "Bearer " + accessToken,
                                        'Content-Type': 'application/json',
                                        'Content-Length': '151', 
                                        'If-None-Match': 'W/"81-IPXBWNB48bs1CNK6NL+XgeHJooA"',
                                        "proxy": f"http://{self.proxy}"
                                        }
                                )

    @check_gas
    @retry
    async def mintNft(self):
        logger.info(f"[{self.account_id}][{self.address}] МинтSidus")
        self.registerWallet()
        self.getTokenData()
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

    @check_gas
    @retry
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