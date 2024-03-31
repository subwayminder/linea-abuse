from config import FROG_WAR_CONTRACT, FROG_WAR_ABI, FROG_WAR_CLAIM_METHOD_ID
from ..account import Account
from typing import Union
from hashlib import sha256
from typing import Union
from loguru import logger
from utils.gas_checker import check_gas
from eth_account.messages import encode_defunct
from utils.helpers import retry


class FrogWar(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)
        self.contract = self.get_contract(FROG_WAR_CONTRACT, FROG_WAR_ABI)

    @check_gas
    @retry
    async def mintFrogWar(self):
        logger.info(f"[{self.account_id}][{self.address}] Минт Frog War")
        balance = await self.contract.functions.balanceOf(self.address, 1).call()
        if (balance == 0):
            logger.info(f"[{self.account_id}][{self.address}] Frog War free mint")
            txData = await self.getTxData(value=self.w3.to_wei(0.0001, 'ether'))
            txData['data'] = FROG_WAR_CLAIM_METHOD_ID + '000000000000000000000000' + self.address[2:] + '00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee00000000000000000000000000000000000000000000000000005af3107a400000000000000000000000000000000000000000000000000000000000000000e000000000000000000000000000000000000000000000000000000000000001a00000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000000300000000000000000000000000000000000000000000000000005af3107a4000000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
            txData['to'] = FROG_WAR_CONTRACT
            signedTx = await self.sign(txData)
            txHash = await self.send_raw_transaction(signedTx)
            await self.wait_until_tx_finished(txHash.hex())
        else:
            logger.info(f"[{self.account_id}][{self.address}] Frog War NFT уже сминчена")