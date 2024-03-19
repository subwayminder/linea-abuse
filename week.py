import questionary
import json
import time
import random
import asyncio
import sys
from loguru import logger
from web3 import Web3
from web3.middleware import geth_poa_middleware
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from eth_account import Account as EthAccount
from quest_modules.bitavatar import BitAvatar
from questionary import Choice, Separator
from functions import *
from config import ACCOUNTS, PROXIES
from settings import QUANTITY_THREADS, THREAD_SLEEP_FROM, THREAD_SLEEP_TO, USE_PROXY, RANDOM_WALLET, SLEEP_FROM, SLEEP_TO, CHECK_PROXY
from utils.get_proxy import check_proxy
from utils.sleeping import sleep

WEEK_ONE = [
    runGamerBoomSign,
    runTownStorySignUp,
    runTownStoryMintNft,
    runSidusNft,
    runSidiusReleaseNft,
]
WEEK_TWO = [
    runPictographMintNft,
    runSatoshiNftMint,
    runAbyssNftMint,
]
WEEK_THREE = [
    runDmailSend,
    runBitAvatarCheckIn,
    runGamicDepositWeth,
    runEmeraldMintNft,
    runReadonCurate,
    runSendingMeTx,
    runAbyssNftMint,
]
WEEK_FOUR = [
    runTanukiNftMint,
    runLuckyCat,
]
WEEK_FIVE = [
    runBattlemonMintNft,
    runNftBadgeMint
]
WEEK_SIX = []
ALL_IN = [
    runGamerBoomSign,
    runTownStorySignUp,
    runTownStoryMintNft,
    runSidusNft,
    runSidiusReleaseNft,
    runPictographMintNft,
    runSatoshiNftMint,
    runAbyssNftMint,
    runDmailSend,
    runBitAvatarCheckIn,
    runGamicDepositWeth,
    runEmeraldMintNft,
    runReadonCurate,
    runSendingMeTx,
    runAbyssNftMint,
    runTanukiNftMint,
    runLuckyCat,
    runBattlemonMintNft,
    runNftBadgeMint,
]

def getWallets():
    if USE_PROXY:
        account_with_proxy = dict(zip(ACCOUNTS, PROXIES))

        wallets = [
            {
                "id": _id,
                "key": key,
                "proxy": account_with_proxy[key]
            } for _id, key in enumerate(account_with_proxy, start=1)
        ]
    else:
        wallets = [
            {
                "id": _id,
                "key": key,
                "proxy": None
            } for _id, key in enumerate(ACCOUNTS, start=1)
        ]
    return wallets

def get_week():
    result = questionary.select(
        "Выбор опций",
        choices=[
            Choice("1-я неделя", WEEK_ONE),
            Choice("2-я неделя", WEEK_TWO),
            Choice("3-я неделя", WEEK_THREE),
            Choice("4-я неделя", WEEK_FOUR),
            Choice("5-я неделя", WEEK_FIVE),
            Choice("Все недели", ALL_IN),
            Choice("Exit", "exit"),
        ],
        qmark="⚙️ ",
        pointer="🤡 "
    ).ask()
    if result == "exit":
        print("Ну все давай пока 🤡")
        sys.exit()
    return result

async def run_module(module, account):
    try:
        await module(account)
    except Exception as e:
        logger.error(f"[{module}] " + e)

    # if REMOVE_WALLET:
    #     remove_wallet(key)

    await sleep(SLEEP_FROM, SLEEP_TO)

def _async_run_module(module, account):
    asyncio.run(run_module(module, account))

def main(week):
    if(CHECK_PROXY):
        for proxy in PROXIES:
            checkProxy = asyncio.run(check_proxy(proxy))
            if(checkProxy != True):
                raise ValueError('Прокси ' + proxy + ' не работает')

    wallets = getWallets()

    if RANDOM_WALLET:
        random.shuffle(wallets)

    with ProcessPoolExecutor(max_workers=QUANTITY_THREADS) as executor:
        for _, account in enumerate(wallets, start=1):
            for _, module in enumerate(week, start=1):
                executor.submit(
                    _async_run_module,
                    module,
                    account
                )
                time.sleep(random.randint(THREAD_SLEEP_FROM, THREAD_SLEEP_TO))

if __name__ == '__main__':
    logger.add("logging.log")
    week = get_week()
    main(week)