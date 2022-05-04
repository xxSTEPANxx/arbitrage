from terra_sdk.client.lcd.api.wasm import WasmAPI
from terra_sdk.client.lcd.lcdclient import LCDClient, LCDResponseError

import requests
from json import load, dump

terra = LCDClient("https://lcd.terra.dev", "columbus-5")
wasm = WasmAPI(terra)


symbols = {}
natives = {}


def get_symbols_from_asset_infos(asset_infos: dict):
    """
    :param pair: asset_infos from the dict the way dex router gives information about a pool.
    :return: updates global symbols dict
    """
    for asset_info in asset_infos:
        for key in asset_info.keys():
            if key == "token":
                token_addr = asset_info[key]['contract_addr']
                symbol = get_symbol_by_contract(token_addr)
                symbols[symbol] = token_addr
            else:
                token_denom = asset_info[key]['denom']
                natives[token_denom] = [token_denom]


def get_symbol_by_contract(contract: str):
    """
    :param contract: CW20_token
    :return: tokens symbol
    """
    try:
        return wasm.contract_info(contract)["init_msg"].get('symbol', 'not_a_token')
    except LCDResponseError:
        return "not_a_token"


def get_contract_by_symbol(symbol: str, symbols: dict):
    """
    :param cymbol: token simbol
    :param symbols: dict of known simbols. from json or global memory
    :return: contract: str if token exists else None
    """
    return symbols.get(symbol, None)


with open("json_files//all_astroport_contracts.json") as file:
    pairs = load(file)
for pair in pairs:
    asset_infos = pair["asset_infos"]
    get_symbols_from_asset_infos(asset_infos)
print(symbols)
print(natives)