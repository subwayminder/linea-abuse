import random

from config import RPC
from web3 import Web3
from loguru import logger


async def check_proxy(proxy):
    request_kwargs = {"proxies": {"https": f"http://{proxy}"}}
    w3 = Web3(Web3.HTTPProvider(RPC, request_kwargs=request_kwargs))
    if w3.is_connected():
        logger.info(f"Прокси [http://{proxy}] работает")
        return True
    return False
