import simulations
import config

from terra_sdk.exceptions import LCDResponseError
from terra_sdk.client.lcd.lcdclient import LCDClient
from terra_sdk.client.lcd.api.wasm import WasmAPI

terra = LCDClient("https://lcd.terra.dev", "columbus-5")
wasm = WasmAPI(terra)

res = simulations.simulation(wasm, config.astroport_router, 10, *('terra15gwkyepfc6xgca5t5zefzwy42uts8l2m4g40k6', 'uusd', 'uluna'))
print(res)
