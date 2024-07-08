import json

WALLET_DATA_PATH = 'wallet_data.xlsx'
SHEET_NAME = 'evm'
ENCRYPTED_DATA_PATH = 'encrypted_data.txt'
REALTIME_SETTINGS_PATH = 'realtime_settings.json'
PROGRESS_PATH = 'progress.xlsx'

with open('data/rpc.json') as file:
    RPC = json.load(file)

with open('data/abi/erc20_abi.json') as file:
    ERC20_ABI = json.load(file)

with open("data/abi/dmail/abi.json", "r") as file:
    DMAIL_ABI = json.load(file)

with open('data/orbiter_maker.json', 'r') as file:
    ORBITER_MAKER = json.load(file)

with open('data/abi/nidum/abi.json', "r") as file:
    NIDUM_ABI = json.load(file)

with open('data/abi/townstory/abi.json', "r") as file:
    TOWNSTORY_ABI = json.load(file)

with open('data/abi/townstory/travelvag_abi.json', "r") as file:
    TOWNSTORY_TRAVELBAG_ABI = json.load(file)

with open('data/abi/alienswap/abi.json', 'r') as file:
    ALIENSWAP_ABI = json.load(file)

with open('data/abi/pictographs/abi.json', 'r') as file:
    PICTOGRAPHS_ABI = json.load(file)

with open('data/abi/omnisea/abi.json', 'r') as file:
    OMNISEA_ABI = json.load(file)

with open('data/abi/weth/abi.json', 'r') as file:
    WETH_ABI = json.load(file)

with open('data/abi/readon/abi.json', 'r') as file:
    READON_ABI = json.load(file)

with open('data/abi/lucky_cat/abi.json', 'r') as file:
    LUCKY_CAT_ABI = json.load(file)

with open('data/abi/nouns/abi.json', 'r') as file:
    NOUNS_ABI = json.load(file)

with open('data/abi/micro3/abi.json', 'r') as file:
    MICRO3_ABI = json.load(file)

with open('data/abi/frog_war/abi.json', 'r') as file:
    FROG_WAR_ABI = json.load(file)

with open('data/abi/bilinear/abi.json', 'r') as file:
    BILINEAR_ABI = json.load(file)

with open('data/abi/imaginairynfts/abi.json', 'r') as file:
    IMAGINEAI_ABI = json.load(file)

with open('data/abi/arenagames/abi.json', 'r') as file:
    ARENAGAMES_ABI = json.load(file)

with open('data/abi/layerbank/abi.json', 'r') as file:
    LAYERBANK_ABI = json.load(file)

with open('data/abi/octomos/abi.json', 'r') as file:
    OCTOMOS_ABI = json.load(file)

with open('data/abi/clutchai/abi.json', 'r') as file:
    CRAZYGANG_ABI = json.load(file)

with open('data/abi/mintpad/abi.json', 'r') as file:
    MINTPAD_ABI = json.load(file)

with open('data/abi/wizards/abi.json', 'r') as file:
    WIZARDS_ABI = json.load(file)

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"
LAYERBANK_CONTRACT = "0x43Eac5BFEa14531B8DE0B334E123eA98325de866"
LAYERBANK_WETH_CONTRACT = "0x9E9aec6a296f94C8530e2dD01FF3E9c61555D39a"


DMAIL_CONTRACT = "0xD1A3abf42f9E66BE86cfDEa8c5C2c74f041c5e14"
NIDUM_CONTRACT = "0x34be5b8c30ee4fde069dc878989686abe9884470"
TOWNSTORY_CONTRACT = "0x281A95769916555D1C97036E0331b232b16EdABC"
TOWNSTORY_TRAVELBAG_CONTRACT = "0xd41ac492fedc671eb965707d1dedad4eb7b6efc5"
ABUSE_WORLD_CONTRACT = "0x0391c15886b5f74a776b404c82d30eef4be88335"
PICTOGRAPHS_CONTRACT = "0xb18b7847072117AE863f71F9473D555d601Eb537"
OMNISEA_CONTRACT = "0xecbee1a087aa83db1fcc6c2c5effc30bcb191589"
ASMATCH_CONTRACT = "0xc043bce9aF87004398181A8de46b26e63B29bf99"
READON_CONTRACT = "0x8286d601a0ed6cf75E067E0614f73A5b9F024151"
SARUBOL_CONTRACT = "0x6cada4ccec51d7f40747be4a087520f02dde9f48"
ZYPHER_CONTRACT = "0x490d76b1e9418a78b5403740bd70dfd4f6007e0f"
LUCKY_CAT_CONTRACT = "0xc577018b3518cD7763D143d7699B280d6E50fdb6"
OMNIZONE_CONTRACT = "0x7136Abb0fa3d88E4B4D4eE58FC1dfb8506bb7De7"
BATTLEMON_CONTRACT = "0x578705C60609C9f02d8B7c1d83825E2F031e35AA"
UNFETTERED_CONTRACT = "0x2dC9D44eC35d5DEfD146e5fD718eE3277dfaCF0A"
NOUNS_CONTRACT = "0x9DF3c2C75a92069B99c73bd386961631F143727C"
MICRO3_CONTRACT = "0x915d2358192f5429fa6ee6a6e5d1b37026d580ba"
ALIENSWAP_CONTRACT = "0x5EcDe77C11E52872aDeB3Ef3565Ffa0B2BCC1C68"
FROG_WAR_CONTRACT = "0xEA81a18fb97401A9F4B79963090c65a3A30ECdce"
WARRIOR_CONTRACT = "0x184e5677890c5add563de785ff371f6c188d3db6"
BILINEAR_CONTRACT = "0xA091303966Ef5F94Cf68F85d892c729fd6c3F30B"
IMAGINEAI_CONTRACT = "0xb99e5534d42500eb1d5820fba3bb8416ccb76396"
ARENAGAMES_CONTRACT = "0xbd0ef89f141680b9b2417e4384fdf73cfc696f9f"
OCTOMOS_CONTRACT = "0xBcFa22a36E555c507092FF16c1af4cB74B8514C8"
CRAZYGANG_CONTRACT = "0xB8DD4f5Aa8AD3fEADc50F9d670644c02a07c9374"
MINTPAD_CONTRACT = "0x3685102bc3D0dd23A88eF8fc084a8235bE929f1c"
WIZARDS_CONTRACT = "0xD540038B0B427238984E0341bA49F69CD80DC139"
EFROGS_CONTRACT = "0xf4AA97cDE2686Bc5ae2Ee934a8E5330B8B13Be64"
SATOSHI_UNIVERSE_CONTRACT = "0xc0A2a606913A49a0B0a02F682C833EFF3829B4bA"


LINEA_TOKENS = {
    "WETH": "0xe5D7C2a44FfDDf6b295A15c148167daaAf5Cf34f",
    "USDC": "0x176211869cA2b568f2A7D4EE941E073a821EE1ff",
    "LXP": "0xd83af4fbd77f3ab65c3b1dc4b38d7e67aecf599a"
}


LINEASCAN_URL = 'https://api.lineascan.build/api'

LINEA_API_KEYS = ['']  # ['api_key1', 'api_key2'], api keys from https://lineascan.build

CHAINS_OKX = {
    'linea': 'Linea',
    'base': 'Base',
    'arbitrum': 'Arbitrum One',
    'optimism': 'Optimism',
    'zksync': 'zkSync Era'
}

ORBITER_CHAINS_INFO = {
    1: {'name': 'Arbitrum', 'chainId': 42161, 'id': 2},
    2: {'name': 'Arbitrum Nova', 'chainId': 42170, 'id': 16},
    3: {'name': 'Base', 'chainId': 8453, 'id': 21},
    4: {'name': 'Linea', 'chainId': 59144, 'id': 23},
    5: {'name': 'Manta', 'chainId': 169, 'id': 31},
    6: {'name': 'Polygon', 'chainId': 137, 'id': 6},
    7: {'name': 'Optimism', 'chainId': 10, 'id': 7},
    8: {'name': 'Scroll', 'chainId': 534352, 'id': 19},
    9: {'name': 'Starknet', 'chainId': 'SN_MAIN', 'id': 4},
    10: {'name': 'Polygon zkEVM', 'chainId': 1101, 'id': 17},
    11: {'name': 'zkSync Era', 'chainId': 324, 'id': 14},
    12: {'name': 'Zora', 'chainId': 7777777, 'id': 30},
    13: {'name': 'Ethereum', 'chainId': 1, 'id': 1},
    14: {'name': 'BNB Chain', 'chainId': 56, 'id': 15},
    26: {'name': 'Metis', 'chainId': 1088, 'id': 10},
    28: {'name': 'OpBNB', 'chainId': 204, 'id': 25},
    29: {'name': 'Mantle', 'chainId': 5000, 'id': 24},
    45: {'name': 'ZKFair', 'chainId': 42766, 'id': 38}
}

LAYERZERO_WRAPED_NETWORKS = {
    1: 1,
    2: 2,
    3: 27,
    4: 34,
    5: 14,
    6: 15,
    7: 3,
    8: 35,
    9: 19,
    10: 23,
    11: 21,
    12: 36,
    13: 13,
    14: 33,
    15: 37,
    16: 38,
    17: 20,
    18: 17,
    19: 25,
    20: 32,
    21: 31,
    22: 4,
    23: 44,
    24: 5,
    25: 29,
    26: 39,
    27: 26,
    28: 16,
    29: 30,
    30: 40,
    31: 7,
    32: 24,
    33: 6,
    34: 10,
    35: 8,
    36: 41,
    37: 18,
    38: 22,
    39: 42,
    40: 43,
    41: 12,
    42: 28,
    43: 11,
    44: 46
}

HEADER = """
██╗     ██╗███╗   ██╗███████╗ █████╗     ██████╗  █████╗ ██████╗ ██╗  ██╗
██║     ██║████╗  ██║██╔════╝██╔══██╗    ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝
██║     ██║██╔██╗ ██║█████╗  ███████║    ██████╔╝███████║██████╔╝█████╔╝ 
██║     ██║██║╚██╗██║██╔══╝  ██╔══██║    ██╔═══╝ ██╔══██║██╔══██╗██╔═██╗ 
███████╗██║██║ ╚████║███████╗██║  ██║    ██║     ██║  ██║██║  ██║██║  ██╗
╚══════╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝                                                                         
"""
