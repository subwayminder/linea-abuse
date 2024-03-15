from quest_modules.bitavatar import BitAvatar
from quest_modules.dmail import Dmail
from quest_modules.week2.pictograph import Pictograph
from quest_modules.gamic import Gamic
from quest_modules.emerald_nft import EmeraldNft
from quest_modules.readon import ReadOn
from quest_modules.account import Account
from quest_modules.week2.abyss_nft import AbyssNft
from quest_modules.week2.enders_gate import EndersGate
from quest_modules.week2.yooldoo import Yooldoo
from quest_modules.week4.tanuki import TanukiNft
from config import SENDING_ME_FAKE_WALLET, SATOSHI_FAKE_WALLET
from eth_account.messages import encode_defunct
from web3 import Web3
import uuid
import requests
import time

async def runBitAvatarCheckIn(account):
    bitAvatarModule = BitAvatar(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await bitAvatarModule.checkIn()

async def runDmailSend(account):
    dmailModule = Dmail(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await dmailModule.sendMail()

async def runPictographMintNft(account):
    pictographModule = Pictograph(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await pictographModule.mintNft()

async def runGamicDepositWeth(account):
    gamicModule = Gamic(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await gamicModule.depositWeth()

async def runEmeraldMintNft(account):
    emeraldModule = EmeraldNft(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await emeraldModule.mintNft()

async def runReadonCurate(account):
    readonModule = ReadOn(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await readonModule.curate()

async def runSendingMeTx(account):
    accountInstance = Account(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    tx = {
            "chainId": await accountInstance.w3.eth.chain_id,
            "from": accountInstance.address,
            "to": SENDING_ME_FAKE_WALLET,
            "value": 100000000000000,
            "gasPrice": await accountInstance.w3.eth.gas_price,
            "nonce": await accountInstance.w3.eth.get_transaction_count(accountInstance.address),
        }
    signedTx = await accountInstance.sign(tx)
    txHash = await accountInstance.send_raw_transaction(signedTx)
    await accountInstance.wait_until_tx_finished(txHash.hex())

async def runAbyssNftMint(account):
    abyssModule = AbyssNft(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await abyssModule.mintNft()

async def runEndersGateMint(account):
    endersNftModule = EndersGate(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await endersNftModule.mintNft()

async def runSatoshiNftMint(account):
    accountInstance = Account(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    tx = {
            "chainId": await accountInstance.w3.eth.chain_id,
            "from": accountInstance.address,
            "to": SATOSHI_FAKE_WALLET,
            "value": 100000000000000,
            "gasPrice": await accountInstance.w3.eth.gas_price,
            "nonce": await accountInstance.w3.eth.get_transaction_count(accountInstance.address),
        }
    signedTx = await accountInstance.sign(tx)
    txHash = await accountInstance.send_raw_transaction(signedTx)
    await accountInstance.wait_until_tx_finished(txHash.hex())

async def runYooldoo(account):
    module = Yooldoo(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await module.run()

async def runTanukiNftMint(account):
    module = TanukiNft(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await module.mintNft()
