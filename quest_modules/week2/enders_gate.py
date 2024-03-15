from config import ENDERS_GATE_NFT_CONTRACT, ENDERS_GATE_NFT_ABI
from ..account import Account
from typing import Union
from hashlib import sha256
from typing import Union
from loguru import logger
from hexbytes import HexBytes
from utils.gas_checker import check_gas
from utils.helpers import retry


class EndersGate(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)
        self.contract = self.get_contract(ENDERS_GATE_NFT_CONTRACT, ENDERS_GATE_NFT_ABI)

    @check_gas
    @retry
    async def mintNft(self):
        txData = await self.getTxData()
        tx = await self.contract.functions.mint('0x8b546451aA616000f2dB48c7B94Bd7bCEEcF44c2', 1, 1).build_transaction(txData)
        signedTx = await self.sign(tx)
        txHash = await self.send_raw_transaction(signedTx)
        await self.wait_until_tx_finished(txHash.hex())