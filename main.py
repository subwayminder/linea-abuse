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
from questionary import Choice, Separator
from functions import *
from config import ACCOUNTS, PROXIES
from settings import QUANTITY_THREADS, THREAD_SLEEP_FROM, THREAD_SLEEP_TO, USE_PROXY, RANDOM_WALLET, SLEEP_FROM, SLEEP_TO, CHECK_PROXY
from utils.get_proxy import check_proxy
from utils.sleeping import sleep

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
            Choice("Минт Sidus", runSidusNft),
            Choice("Sidus - релиз сминченой NFT", runSidiusReleaseNft),
            Choice("GamerBoom", runGamerBoomSign),
            Choice("Town Story регистрация", runTownStorySignUp),
            Choice("Town Story минт", runTownStoryMintNft),
            Separator(" - 2-я неделя"),
            Choice("Минт Pictogram NFT", runPictographMintNft),
            Choice("Стейкинг Pictogram", runPictographStake),
            Choice("Минт Satoshi NFT", runSatoshiNftMint),
            Choice("Минт Enders Gate", runEndersGateMint),
            Choice("Минт Abyss NFT", runAbyssNftMint),
            Choice("Yooldoo Stand Up", runYooldoo),
            Separator(" - 3-я неделя"),
            Choice("Отправить письмо Dmail", runDmailSend),
            Choice("BitAvatar чекин", runBitAvatarCheckIn),
            Choice("Gamic WETH депозит", runGamicDepositWeth),
            Choice("Минтим Emerald NFT", runEmeraldMintNft),
            Choice("Курируем ссылку на ReadOn", runReadonCurate),
            Choice("Делаем транзу для SendingMe", runSendingMeTx),
            Separator(" - 4-я неделя"),
            Choice("Минтим Tanuki", runTanukiNftMint),
            Choice("Lucky Cat", runLuckyCat),
            Choice("Zypher 2048", runZypher),
            Separator(" - 5-я неделя"),
            Choice("Минтим Battlemon Nft", runBattlemonMintNft),
            Choice("Минтим Nft Badge", runNftBadgeMint),
            Choice("Клеймим Nouns", runNounsClaim),
            Separator(" - 6-я неделя"),
            Choice("Минтим Zace", runZaceMint),
            Choice("Минтим Micro3", runMicro3Mint),
            Choice("Минтим Alien Linea", runAlienLineaMint),
            Choice("Листинг на Alien", runAlienListing),
            Choice("Минт Frog War", runFrogWarMint),
            Choice("Минт Frog War Warrior", runFrogWarWarriorMint),
            Choice("Frog War Warrior - send to battle", runFrogWarWarriorSendToBattle),
            Choice("Минт Acg Worlds", runAcgWorldsMint),
            Choice("Минт Imaginalry", runImaginalryMint),
            Choice("Минт Arena", runArenaMint),
            # Choice("Минт через Element", runElementMint),
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

# Для тестовых запусков
def test_run(module):
    wallets = getWallets()
    for _, account in enumerate(wallets, start=1):
        asyncio.run(module(account))
        sys.exit('Bye')

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

    with ProcessPoolExecutor(max_workers=QUANTITY_THREADS) as executor:
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