import questionary
import json
import time
import random
import asyncio
import sys
from loguru import logger
from web3 import Web3
from web3.middleware import geth_poa_middleware
from concurrent.futures import ThreadPoolExecutor
from eth_account import Account as EthAccount
from quest_modules.bitavatar import BitAvatar
from questionary import Choice, Separator
from functions import *
from config import ACCOUNTS, PROXIES
from settings import QUANTITY_THREADS, THREAD_SLEEP_FROM, THREAD_SLEEP_TO, USE_PROXY, RANDOM_WALLET, SLEEP_FROM, SLEEP_TO, CHECK_PROXY
from utils.get_proxy import check_proxy

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

def get_module():
    result = questionary.select(
        "Выбор опций",
        choices=[
            # TODO: разобрать Sonorus signup
            Separator(" - 1-я неделя"),
            Choice("Минт Pictogram NFT", runSidusNft),
            Choice("Минт Pictogram NFT", runGamerBoomSign),
            Choice("Минт Pictogram NFT", runTownStorySignUp),
            Choice("Минт Pictogram NFT", runTownStoryMintNft),
            Choice("Минт Pictogram NFT", runTownStoryReleaseNft),
            Separator(" - 2-я неделя"),
            Choice("Минт Pictogram NFT", runPictographMintNft),
            Choice("Минт Satoshi NFT", runSatoshiNftMint),
            Choice("Минт Abyss NFT", runAbyssNftMint),
            # TODO: Доделать enders gate по возможности
            # Choice("Минтим Enders Gate", runEndersGateMint),
            Separator(" - 3-я неделя"),
            Choice("Отправить письмо Dmail", runDmailSend),
            Choice("BitAvatar чекин", runDmailSend),
            Choice("Gamic WETH депозит", runGamicDepositWeth),
            Choice("Минтим Emerald NFT", runEmeraldMintNft),
            Choice("Курируем ссылку на ReadOn", runReadonCurate),
            Choice("Делаем транзу для SendingMe", runSendingMeTx),
            Choice("Минтим Abyss", runAbyssNftMint),
            Separator(" - 4-я неделя"),
            Choice("Минтим Tanuki", runTanukiNftMint),
            Choice("Lucky Cat", runLuckyCat),
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
        logger.error(e)

    if REMOVE_WALLET:
        remove_wallet(key)

    await sleep(SLEEP_FROM, SLEEP_TO)

# Для тестовых запусков
def test_run(module):
    wallets = getWallets()
    for _, account in enumerate(wallets, start=1):
        asyncio.run(module(account))

def _async_run_module(module, account):
    asyncio.run(run_module(module, account))

def main(module):
    if(CHECK_PROXY):
        for proxy in PROXIES:
            checkProxy = asyncio.run(check_proxy(proxy))
            if(checkProxy != True):
                raise ValueError('Прокси ' + proxy + ' не работает')

    wallets = getWallets()

    if RANDOM_WALLET:
        random.shuffle(wallets)

    with ThreadPoolExecutor(max_workers=QUANTITY_THREADS) as executor:
        for _, account in enumerate(wallets, start=1):
            executor.submit(
                _async_run_module,
                module,
                account
            )
            time.sleep(random.randint(THREAD_SLEEP_FROM, THREAD_SLEEP_TO))

if __name__ == '__main__':
    logger.add("logging.log")
    module = get_module()
    main(module=module)