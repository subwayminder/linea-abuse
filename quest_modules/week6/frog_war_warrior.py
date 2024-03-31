from config import FROG_WAR_WARRIOR_CONTRACT, FROG_WAR_WARRIOR_ABI, FROG_WAR_WARRIOR_CLAIM_METHOD_ID, FROG_WAR_RELEASE_OPERATOR
from ..account import Account
from typing import Union
from hashlib import sha256
from typing import Union
from loguru import logger
from utils.gas_checker import check_gas
from eth_account.messages import encode_defunct
from utils.helpers import retry


class FrogWarWarrior(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)
        self.contract = self.get_contract(FROG_WAR_WARRIOR_CONTRACT, FROG_WAR_WARRIOR_ABI)

    @check_gas
    @retry
    async def mintFrogWarWarrior(self):
        logger.info(f"[{self.account_id}][{self.address}] Минт Frog War Warrior")
        balance = await self.contract.functions.balanceOf(self.address, 6).call()
        if (balance == 0):
            txData = await self.getTxData()
            txData['data'] = FROG_WAR_WARRIOR_CLAIM_METHOD_ID + '000000000000000000000000' + self.address[2:] + '0000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000100000000000000000000000021d624c846725abe1e1e7d662e9fb274999009aa000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e000000000000000000000000000000000000000000000000000000000000001a000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000021d624c846725abe1e1e7d662e9fb274999009aa000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
            txData['to'] = FROG_WAR_WARRIOR_CONTRACT
            signedTx = await self.sign(txData)
            txHash = await self.send_raw_transaction(signedTx)
            await self.wait_until_tx_finished(txHash.hex())
        else:
            logger.info(f"[{self.account_id}][{self.address}] Frog War Warrior NFT уже сминчена")

    @check_gas
    @retry
    async def sendToBattle(self):
        logger.info(f"[{self.account_id}][{self.address}] Frog War Warrior - send to battle")
        balance = await self.contract.functions.balanceOf(self.address, 6).call()
        if(balance != 0):
            txData = await self.getTxData()
            tx = await self.contract.functions.setApprovalForAll(FROG_WAR_RELEASE_OPERATOR, True).build_transaction(txData)
            signedTx = await self.sign(tx)
            txHash = await self.send_raw_transaction(signedTx)
            await self.wait_until_tx_finished(txHash.hex())
        else:
            logger.info(f"[{self.account_id}][{self.address}] Frog War Warrior NFT еще не сминчена")