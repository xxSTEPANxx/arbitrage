from terra_sdk.exceptions import LCDResponseError
from terra_sdk.client.lcd.lcdclient import LCDClient
from terra_sdk.client.lcd.api.wasm import WasmAPI

import copy
import json


terra = LCDClient("https://lcd.terra.dev", "columbus-5")
# terra = LCDClient("https://bombay-lcd.terra.dev", "bombay-12")
wasm = WasmAPI(terra)


astroport_factory = "terra1fnywlw4edny3vw44x04xd67uzkdqluymgreu7g"
terraswap_factory = "terra1ulgw0td86nvs4wtpsc80thv6xelk76ut7a7apj"
loop_factory = "terra16hdjuvghcumu6prg22cdjl96ptuay6r0hc6yns"
dex_names = {terraswap_factory: "terraswap", astroport_factory: "astroport", loop_factory: "loop"}
query_msg = {"pairs": {"limit": 30}}

path = "json_files/"

def get_dex_pairs(dex_factory):
    print(f"start creating pairs list for {dex_names[dex_factory]}")
    pairs = wasm.contract_query(dex_factory, query_msg)["pairs"]
    all_pairs = []
    all_pairs.extend(pairs)

    while len(pairs) == 30:
        new_query_msg = copy.deepcopy(query_msg)
        new_query_msg["pairs"]["start_after"] = pairs[-1]["asset_infos"]

        new_pairs = wasm.contract_query(dex_factory, new_query_msg)["pairs"]
        if new_pairs == pairs:
            break
        all_pairs.extend(new_pairs)
        pairs = new_pairs

    with open(path + f"all_{dex_names[dex_factory]}_contracts.json", "w") as file:
        json.dump(all_pairs, file, indent=4)

    print("got", len(all_pairs), "pair contracts")


def get_symbols(dex_factory):

    print("start gettting symbols from", dex_names[dex_factory])
    with open(path + f"all_{dex_names[dex_factory]}_contracts.json", "r") as all_pairs_json:
        all_pairs = json.load(all_pairs_json)

        symbols = {}
        native_denoms = {}
        graf = {}

        for pair in all_pairs:
            token_1 = pair["asset_infos"][0]
            token_2 = pair["asset_infos"][1]

            if tuple(token_1.keys())[0] == "token":
                try:
                    info = wasm.contract_info(token_1["token"]["contract_addr"])["init_msg"]
                except LCDResponseError:
                    info = {}
                symbol = info.get("symbol", "not_a_token")
                symbols[symbol] = token_1["token"]["contract_addr"]
            else:
                native_denoms[token_1["native_token"]["denom"]] = token_1["native_token"]["denom"]

            if tuple(token_2.keys())[0] == "token":
                try:
                    info = wasm.contract_info(token_2["token"]["contract_addr"])["init_msg"]
                except LCDResponseError:
                    info = {}
                symbol = info.get("symbol", "not_a_token")
                symbols[symbol] = token_2["token"]["contract_addr"]
            else:
                native_denoms[token_2["native_token"]["denom"]] = token_2["native_token"]["denom"]
    return symbols, native_denoms

    # with open("symbols.json", "r") as file:
    #     old_symbols = json.load(file)
    #     old_symbols.update(symbols)
    # with open("symbols.json", "w") as file:
    #     json.dump(old_symbols, file, indent=4)
    #
    # with open("natives.json", "r") as file:
    #     old_natives = json.load(file)
    #     old_natives.update(native_denoms)
    # with open("natives.json", "w") as file:
    #     json.dump(old_natives, file, indent=4)
    # print(f"done with {dex_names[dex_factory]}, got {len(old_symbols) - len(symbols)} new symbols")

def get_all_symbols(dex_names):
    all_symbols = {}
    all_natives = {}
    for dex in dex_names:
        symbols, natives = get_symbols(dex)
        all_symbols.update(symbols)
        all_natives.update(natives)
    with open(path + "symbols.json", "w") as file:
        json.dump(all_symbols, file, indent=4)
    with open(path + "natives.json", "w") as file:
        json.dump(all_natives, file, indent=4)

# get_dex_pairs(astroport_factory)

# try:
#     a = wasm.contract_info("terra1pg606jw68d9mnh9czrgm7celc3rq9x5wrvj7gl")["init_msg"]
# except LCDResponseError:
#     a = "got you"
# print(a)



for dex in dex_names:
     get_dex_pairs(dex)
get_all_symbols(dex_names)
#     get_symbols(dex)
# terra_sdk.exceptions.LCDResponseError:
# Status 404 - {'code': 5, 'message': 'rpc error: code = NotFound desc =
# constractInfo terra1pg606jw68d9mnh9czrgm7celc3rq9x5wrvj7gl: not found: key not found', 'details': []}

# a = {"a": 10}
# b = {"b": 20}
#
# with open("test.json", "r") as file:
#     dict_test = json.load(file)
#     print(dict_test, type(dict_test), b)
#     dict_test.update(b)
# with open("test.json", "w") as file:
#     json.dump(dict_test, file, indent=4)
