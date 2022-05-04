import graf
import  config

import copy



def create_temlate(dex_factoty: str, tokens: list, amount=None, minimum_receive=None, max_spread=None):
    tp = copy.deepcopy(config.template)
    operations_to_add = []
    swap = config.dex_names[dex_factoty]
    op = {swap: config.operation.copy()}

    for i in range(len(tokens) - 1):

        if tokens[i] in config.native_tokens:
            offer = config.asset_info[1]
            offer["native_token"]["denom"] = tokens[i]
        else:
            offer = config.asset_info[0]
            offer["token"]["contract_addr"] = tokens[i]
        op[swap]["offer_asset_info"] = copy.deepcopy(offer)

        if tokens[i + 1] in config.native_tokens:
            ask = config.asset_info[1]
            ask["native_token"]["denom"] = tokens[i + 1]
        else:
            ask = config.asset_info[0]
            ask["token"]["contract_addr"] = tokens[i + 1]

        op[swap]["ask_asset_info"] = copy.deepcopy(ask)
        operations_to_add.append(copy.deepcopy(op))

    tp["execute_swap_operations"]["operations"] = operations_to_add

    if amount:
        tp["execute_swap_operations"]["offer_amount"] = str(int(amount * config.to_million))
    if minimum_receive:
        tp["execute_swap_operations"]["minimum_receive"] = str(int(minimum_receive * config.to_million))
    if max_spread:
        tp["execute_swap_operations"]["max_spread"] = str(max_spread)
    return tp

print(create_temlate("terra16t7dpwwgx9n3lq6l6te3753lsjqwhxwpday9zx",('terra15gwkyepfc6xgca5t5zefzwy42uts8l2m4g40k6', 'uusd', 'uluna')))

def simulation(wasm, dex, amount, *tokens):
    tp = create_temlate(dex, tokens, amount=amount)
    tp_query = {"simulate_swap_operations": tp["execute_swap_operations"]}
    res = wasm.contract_query(dex, tp_query)
    return res


