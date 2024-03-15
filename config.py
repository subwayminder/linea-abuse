import json
from pathlib import Path
import dotenv
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import sys

ACCOUNTS = []

secret_key = '8b2cf0b5e21ac7abf0e0b7931c5dc13a6960838d36b71af614b2aa81cddebe90'
if not secret_key:
    raise ValueError("The environment variable SECRET_KEY is not set")
secret_key = bytes.fromhex(secret_key)
    

RPC = 'https://rpc.linea.build'
RPC_EXPLOLER = 'https://lineascan.build/tx/'
RPC_TOKEN = 'ETH'

with open('quest_modules/data/erc20_abi.json') as file:
    ERC20_ABI = json.load(file)

with open("accounts.txt", "r") as file:
    while True:
        iv_line = file.readline().strip()
        ct_line = file.readline().strip()
        if not ct_line: break  # End of file
        iv = base64.b64decode(iv_line)
        ct = base64.b64decode(ct_line)
        cipher = AES.new(secret_key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(ct)
        pt = unpad(decrypted, AES.block_size).decode('utf-8')
        ACCOUNTS.append(pt.strip())

if ACCOUNTS.count == 0:
    raise ValueError('Accounts array is empty')

with open("proxy.txt", "r") as file:
    PROXIES = [row.strip() for row in file]

PICTOGRAPHS_CONTRACT = '0xb18b7847072117AE863f71F9473D555d601Eb537'
with open('quest_modules/data/pictographs.json') as file:
    PICTOGRAPHS_ABI = json.load(file)

BITAVATAR_CONTRACT = '0x37D4BFc8c583d297A0740D734B271eAc9a88aDe4'
with open('quest_modules/data/bitavatar.json') as file:
    BITAVATAR_ABI = json.load(file)

DMAIL_CONTRACT = '0xD1A3abf42f9E66BE86cfDEa8c5C2c74f041c5e14'
with open('quest_modules/data/dmail.json') as file:
    DMAIL_ABI = json.load(file)

PICTOGRAPHS_CONTRACT = '0xb18b7847072117AE863f71F9473D555d601Eb537'
with open('quest_modules/data/pictographs.json') as file:
    PICTOGRAPHS_ABI = json.load(file)

GAMIC_CONTRACT = '0xe5D7C2a44FfDDf6b295A15c148167daaAf5Cf34f'
with open('quest_modules/data/gamic.json') as file:
    GAMIC_ABI = json.load(file)

EMERALD_CONTRACT = '0xc043bce9aF87004398181A8de46b26e63B29bf99'
with open('quest_modules/data/emerald_nft.json') as file:
    EMERALD_ABI = json.load(file)

READON_CONTRACT = '0x8286d601a0ed6cf75E067E0614f73A5b9F024151'
with open('quest_modules/data/readon.json') as file:
    READON_ABI = json.load(file)

SENDING_ME_FAKE_WALLET = '0xc0DEb0445e1c307b168478f38eac7646d198F984'

ABYSS_NFT_CONTRACT = '0x66Ccc220543B6832f93c2082EDD7be19c21dF6C0'
with open('quest_modules/data/abyss_nft.json') as file:
    ABYSS_NFT_ABI = json.load(file)

# ENDERS_GATE_NFT_CONTRACT = '0x70Bf27BbB562A9b21FE6EAf2B7832C476691a39f'
ENDERS_GATE_NFT_CONTRACT = '0x967035b7cc9a323c6019fb0b9c53a308d2ca551c'
with open('quest_modules/data/enders_gate.json') as file:
    ENDERS_GATE_NFT_ABI = json.load(file)

SATOSHI_FAKE_WALLET = '0xecbEE1a087aA83Db1fCC6C2C5eFFC30BCb191589'

YOOLDOO_CONTRACT = '0x63ce21BD9af8CC603322cB025f26db567dE8102b'
with open('quest_modules/data/yooldoo.json') as file:
    YOOLDOO_ABI = json.load(file)

TANUKI_CONTRACT = '0x47874ff0BEf601D180a8A653A912EBbE03739a1a'
with open('quest_modules/data/tanuki.json') as file:
    TANUKI_ABI = json.load(file)