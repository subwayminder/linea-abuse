from quest_modules.bitavatar import BitAvatar
from quest_modules.dmail import Dmail
from quest_modules.week2.pictograph import Pictograph
from quest_modules.gamic import Gamic
from quest_modules.emerald_nft import EmeraldNft
from quest_modules.readon import ReadOn
from quest_modules.sending_me import SendingMeTx
from quest_modules.account import Account
from quest_modules.week2.abyss_nft import AbyssNft
from quest_modules.week2.enders_gate import EndersGate
from quest_modules.week2.yooldoo import Yooldoo
from quest_modules.week2.satoshi import SatoshiTx
from quest_modules.week4.tanuki import TanukiNft
from quest_modules.week4.lucky_cat import LuckyCat
from quest_modules.week4.zypher import Zypher
from quest_modules.week4.tomo import TomoNft
from quest_modules.week1.sidus import SidusMint
from quest_modules.week1.gamer_boom import GamerBoom
from quest_modules.week1.town_story import TownStory
from quest_modules.week1.town_story_nft import TownStoryNft
from quest_modules.week5.ntf_badge import NftBadge
from quest_modules.week5.battlemon import BattlemonNft
from quest_modules.week5.nouns import Nouns
from quest_modules.week5.unfettered_expedition import UnfetteredExpeditionNft
from quest_modules.week6.zace import Zace
from quest_modules.week6.micro3 import Micro3
from quest_modules.week6.alien_linea import AlienLinea
from quest_modules.week6.alien_listing import AlienListing
from quest_modules.week6.frog_war import FrogWar
from quest_modules.week6.frog_war_warrior import FrogWarWarrior
from quest_modules.week6.acg_worlds import AcgWorlds
from quest_modules.week6.imaginarly import Imaginalry
from quest_modules.week6.arena import ArenaNft
from quest_modules.week6.element import ElementNft
from config import SENDING_ME_FAKE_WALLET, SATOSHI_FAKE_WALLET
from eth_account.messages import encode_defunct
from utils.gas_checker import check_gas
from utils.helpers import retry
from web3 import Web3
from random import randrange
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

async def runPictographStake(account):
    pictographModule = Pictograph(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await pictographModule.stake()

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
    module = SendingMeTx(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await module.fakeTx()

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
    module = SatoshiTx(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await module.fakeTx()

async def runYooldoo(account):
    module = Yooldoo(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await module.runStandUp()

async def runTanukiNftMint(account):
    module = TanukiNft(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await module.mintNft()

async def runLuckyCat(account):
    module = LuckyCat(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await module.adoptCat()

async def runSidusNft(account):
    module = SidusMint(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await module.mintNft()

async def runGamerBoomSign(account):
    module = GamerBoom(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await module.signGenesisProof()

async def runTownStorySignUp(account):
    module = TownStory(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await module.signUp()

async def runTownStoryMintNft(account):
    module = TownStoryNft(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await module.mintNft()

async def runSidiusReleaseNft(account):
    module = SidusMint(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await module.releaseNft()

async def runBattlemonMintNft(account):
    module = BattlemonNft(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await module.mintNft()

async def runNftBadgeMint(account):
    module = NftBadge(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await module.mintNft()

async def runNounsClaim(account):
    module = Nouns(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await module.claim()

async def runTomoNft(account):
    module = TomoNft(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await module.mintNft()

async def runUnfetteredExpedition(account):
    module = UnfetteredExpeditionNft(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await module.mintNft()

async def runZypher(account):
    module = Zypher(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await module.runTx()

async def runZaceMint(account):
    module = Zace(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await module.mintZace()

async def runMicro3Mint(account):
    module = Micro3(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await module.mintNft()

async def runAlienLineaMint(account):
    module = AlienLinea(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await module.mintNft()

async def runAlienListing(account):
    module = AlienListing(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await module.runListing()

async def runFrogWarMint(account):
    module = FrogWar(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await module.mintFrogWar()

async def runFrogWarWarriorMint(account):
    module = FrogWarWarrior(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await module.mintFrogWarWarrior()

async def runFrogWarWarriorSendToBattle(account):
    module = FrogWarWarrior(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await module.sendToBattle()

async def runAcgWorldsMint(account):
    module = AcgWorlds(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await module.mint()

async def runImaginalryMint(account):
    module = Imaginalry(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await module.mint()

async def runArenaMint(account):
    module = ArenaNft(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await module.mint()

async def runElementMint(account):
    module = ElementNft(
            account_id = account.get('id'), 
            private_key = account.get('key'),
            proxy=account.get('proxy')
        )
    await module.mint()
