import eth_abi
from config import ACG_WORLDS_CONTRACT, ACG_WORLDS_ABI
from ..account import Account
from typing import Union
from loguru import logger
from random import choice
from utils.gas_checker import check_gas
from utils.helpers import retry

class AcgWorlds(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)
        self.contract = self.get_contract(ACG_WORLDS_CONTRACT, ACG_WORLDS_ABI)

    @check_gas
    @retry
    async def mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Acg Worlds минт")
        txData = await self.getTxData(value=self.w3.to_wei(0.0001, 'ether'))
        tx = await self.contract.functions.mint().build_transaction(txData)
        signedTx = await self.sign(tx)
        txHash = await self.send_raw_transaction(signedTx)
        await self.wait_until_tx_finished(txHash.hex())