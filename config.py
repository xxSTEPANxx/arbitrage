native_tokens = {
    "uusd": "uusd",
    "ukrw": "ukrw",
    "usek": "usek",
    "ueur": "ueur",
    "uchf": "uchf",
    "ugbp": "ugbp",
    "uluna": "uluna",
    "uset": "uset",
    "luna": "luna",
    "ust": "ust",
    "umcp": "umcp",
    "ubluna": "ubluna",
    "umnt": "umnt",
    "usdr": "usdr",
    "upepe": "upepe",
    "uust": "uust"
}



asset_info= ({"token":{"contract_addr":""}},{"native_token":{"denom":""}})
operation = {"offer_asset_info": {"token": {"contract_addr": ""}},
                            "ask_asset_info": {"native_token": {"denom": ""}}}
template = {"execute_swap_operations": {}}


path = "json_files/"

astroport_factory = "terra1fnywlw4edny3vw44x04xd67uzkdqluymgreu7g"
terraswap_factory = "terra1ulgw0td86nvs4wtpsc80thv6xelk76ut7a7apj"
loop_factory = "terra16hdjuvghcumu6prg22cdjl96ptuay6r0hc6yns"
astroport_router =  "terra16t7dpwwgx9n3lq6l6te3753lsjqwhxwpday9zx"

dex_names = {terraswap_factory: "terraswap", astroport_router: "astro_swap", loop_factory: "loop"}



to_million = 1000000