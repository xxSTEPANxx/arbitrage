import config
from json import dump, load


def create_graf(dex):
    with open(config.path +"all_astroport_contracts.json", "r") as file:
        all_pairs = load(file)
    graf = dict()
    for pair in all_pairs:

        token_1 = list(list(pair["asset_infos"][0].values())[0].values())[0]
        token_2 = list(list(pair["asset_infos"][1].values())[0].values())[0]

        graf[token_1] = graf.get(token_1, []) +[token_2]
        graf[token_2] = graf.get(token_2, []) + [token_1]
    with open(config.path + "graf.json", "w") as file:
        dump(graf, file, indent=4)

create_graf(1)

def get_contract_by_symbol(symbol):
    if symbol in config.native_tokens:
        return symbol
    with open(config.path + f"symbols.json", 'r') as file:
        symbols = load(file)
        return symbols.get(symbol, None)


def find_paths(token_to, token_from="uusd"):
    token_to = get_contract_by_symbol(token_to)
    token_from = get_contract_by_symbol(token_from)
    paths = []
    paths_to_chek = []
    with open(config.path + f"graf.json", 'r') as file:
        graf = load(file)

    for token1 in graf[token_to]:
        if token1 == token_from:
            paths.append((token_to, token_from))
        else:
            paths_to_chek.append(token1)
        for token1 in paths_to_chek:
            for token2 in graf[token1]:
                if token2 == token_from:
                    paths.append((token_to, token1, token_from))
    print(set(paths))

# create_graf(config.astroport_factory)

find_paths("MIR", "uluna")





