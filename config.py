import json
from pathlib import Path
import dotenv
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import sys
import dotenv

ACCOUNTS = []

secret_key = dotenv.get_key('.env', 'SECRET_KEY')
if not secret_key:
    raise ValueError("The environment variable SECRET_KEY is not set")
secret_key = bytes.fromhex(secret_key)
    

RPC = dotenv.get_key('.env', 'RPC')
RPC_EXPLOLER = dotenv.get_key('.env', 'RPC_EXPLOLER')
RPC_TOKEN = 'ETH'

with open('quest_modules/data/erc20_abi.json') as file:
    ERC20_ABI = json.load(file)

with open("proxy.txt", "r") as file:
    PROXIES = [row.strip() for row in file]

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
YOOLDOO_METHOD_ID = '0xfb89f3b1'
with open('quest_modules/data/yooldoo.json') as file:
    YOOLDOO_ABI = json.load(file)

TANUKI_CONTRACT = '0x47874ff0BEf601D180a8A653A912EBbE03739a1a'
with open('quest_modules/data/tanuki.json') as file:
    TANUKI_ABI = json.load(file)

LUCKY_CAT_CONTRACT = '0xc577018b3518cD7763D143d7699B280d6E50fdb6'
with open('quest_modules/data/lucky_cat.json') as file:
    LUCKY_CAT_ABI = json.load(file)

SIDUS_CONTRACT = '0x34Be5b8C30eE4fDe069DC878989686aBE9884470'
with open('quest_modules/data/sidus.json') as file:
    SIDUS_ABI = json.load(file)

GAMER_BOOM_CONTRACT = '0x6CD20be8914A9Be48f2a35E56354490B80522856'
with open('quest_modules/data/gamer_boom.json') as file:
    GAMER_BOOM_ABI = json.load(file)

TOWN_STORY_CONTRACT = '0x281A95769916555D1C97036E0331b232b16EdABC'
with open('quest_modules/data/town_story.json') as file:
    TOWN_STORY_ABI = json.load(file)

TOWN_STORY_NFT_CONTRACT = '0xD41aC492FEDC671Eb965707d1DEDad4EB7B6EfC5'
with open('quest_modules/data/town_story_nft.json') as file:
    TOWN_STORY_NFT_ABI = json.load(file)

NFT_BADGE_CONTRACT = '0x7136Abb0fa3d88E4B4D4eE58FC1dfb8506bb7De7'
with open('quest_modules/data/nft_badge.json') as file:
    NFT_BADGE_ABI = json.load(file)

BATTLEMON_NFT_CONTRACT = '0x578705C60609C9f02d8B7c1d83825E2F031e35AA'
with open('quest_modules/data/battlemon.json') as file:
    BATTLEMON_NFT_ABI = json.load(file)

NOUNS_CONTRACT = '0x9DF3c2C75a92069B99c73bd386961631F143727C'
with open('quest_modules/data/nouns.json') as file:
    NOUNS_ABI = json.load(file)
NOUNS_CURRENCY = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'

TOMO_CONTRACT = '0x9E813d7661D7B56CBCd3F73E958039B208925Ef8'
with open('quest_modules/data/tomo.json') as file:
    TOMO_ABI = json.load(file)

UNFETTERED_EXPEDITION_NFT_CONTRACT = '0x2dC9D44eC35d5DEfD146e5fD718eE3277dfaCF0A'
with open('quest_modules/data/mint.json') as file:
    UNFETTERED_EXPEDITION_NFT_ABI = json.load(file)

ZYPHER_CONTRACT = '0x490d76B1e9418a78B5403740BD70dfD4F6007E0f'
ZYPHER_METHOD_ID = '0x36ab86c4'

ZACE_CONTRACT='0x971A871Fd8811ABBb1F5e3FB1D84a873d381Cee4'
ZACE_METHOD='0xbaeb0718'

MICRO3_CONTRACT = '0x915D2358192f5429FA6eE6a6e5d1b37026D580Ba'
with open('quest_modules/data/micro3.json') as file:
    MICRO3_ABI = json.load(file)

ALIEN_LINEA_CONTRACT='0x5EcDe77C11E52872aDeB3Ef3565Ffa0B2BCC1C68'
with open('quest_modules/data/alien_linea.json') as file:
    ALIEN_LINEA_ABI = json.load(file)

ALIEN_LISTING_CONTRACT='0x5EcDe77C11E52872aDeB3Ef3565Ffa0B2BCC1C68'
with open('quest_modules/data/alien_listing.json') as file:
    ALIEN_LISTING_ABI = json.load(file)

FROG_WAR_CONTRACT='0xEA81a18fb97401A9F4B79963090c65a3A30ECdce'
with open('quest_modules/data/frog_war.json') as file:
    FROG_WAR_ABI = json.load(file)
FROG_WAR_CLAIM_METHOD_ID='0x57bc3d78'

FROG_WAR_WARRIOR_CONTRACT='0x184E5677890c5aDd563dE785fF371f6c188d3dB6'
with open('quest_modules/data/frog_war_warrior.json') as file:
    FROG_WAR_WARRIOR_ABI = json.load(file)
FROG_WAR_WARRIOR_CLAIM_METHOD_ID='0x57bc3d78'
FROG_WAR_RELEASE_OPERATOR='0x64BE46dE349eb70490fCA494f0D1c3b7dA371870'

ACG_WORLDS_CONTRACT='0xcD1Ea9e70d0260c0F47D217Ed6d5be9Cd4ED34fb'
with open('quest_modules/data/acg_worlds.json') as file:
    ACG_WORLDS_ABI = json.load(file)

IMAGINALRY_CONTRACT='0xb99E5534d42500eB1d5820fBA3Bb8416cCB76396'
with open('quest_modules/data/imaginalry.json') as file:
    IMAGINALRY_ABI = json.load(file)
IMAGINALRY_NFT_LINK='https://ipfs.io/ipfs/bafyreidwx4uav5zivvk7kto2pwszxlcqazqpbxub24zbkk5xzmeiugdap4/metadata.json'

ARENA_CONTRACT='0xbd0ef89f141680b9b2417e4384fdf73cfc696f9f'
with open('quest_modules/data/arena_nft.json') as file:
    ARENA_ABI = json.load(file)