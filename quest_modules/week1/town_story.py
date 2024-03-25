from config import TOWN_STORY_CONTRACT, TOWN_STORY_ABI
from ..account import Account
from typing import Union
from hashlib import sha256
from typing import Union
from loguru import logger
from utils.gas_checker import check_gas
from utils.helpers import retry
from eth_account.messages import encode_defunct
import requests
import sys
import time


class TownStory(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)
        self.contract = self.get_contract(TOWN_STORY_CONTRACT, TOWN_STORY_ABI)
    
    def getSign(self):
        nonce = int(int(time.time()) / 86400)
        address = str(self.address).lower()
        address = address[0:19] + '...' + address[24:]
        msgText = 'Welcome to Town Story! \n\nClick to sign in and accept the Town Story\nTerms of Service:\nhttps://townstory.io/\n\nThis request will not trigger a blockchain\ntransaction or cost any gas fees.\n\nYour authentication status will reset after\neach session.\n\nWallet address:\n'
        msgText = msgText + address + "\n\nNonce: " + str(nonce)
        message = encode_defunct(text=msgText)
        sign = self.w3.eth.account.sign_message(message, private_key=self.private_key).signature
        return sign

    @retry
    @check_gas
    async def signUp(self):
        logger.info(f"[{self.account_id}][{self.address}] Регистрация в Town Story")
        sign = self.getSign().hex()
        loginRequest = requests.post(url='https://aws-login.townstory.io/town-login/handler.php', json={
            "transaction":{
                "func": "register.loginByWallet",
                "params": {
                    "hall": 0,
                    "address": self.address,
                    "wallet":"metamask",
                    "signature": sign,
                    "chain": "linea"
                }
            },
            "header":{
                "baseVersion":"1.0.0",
                "referer":"",
                "version":"1.0.1"
            }
        })
        loginResponse = loginRequest.json()
        if('signature' in loginResponse['response']):
            signForSignUp = loginResponse['response']['signature']
            deadline = loginResponse['response']['deadline']
            txData = await self.getTxData()
            tx = await self.contract.functions.createAccountSign(signForSignUp, 0, int(deadline)).build_transaction(txData)
            signedTx = await self.sign(tx)
            txHash = await self.send_raw_transaction(signedTx)
            await self.wait_until_tx_finished(txHash.hex())
        elif('sig' in loginResponse['response']['auth']):
            logger.info(f"[{self.account_id}][{self.address}] Регистрация в Town Story - уже зарегистрирован")
        elif('failed' in loginResponse):
            raise RuntimeError('Регистрация в Town Story - ошибка регистрации')
        else:
            raise RuntimeError('Регистрация в Town Story - ошибка регистрации')