import network
import time

from config import (
    WIFI_SSID,
    WIFI_PASSWORD
)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

print(f'Connecting to: {WIFI_SSID}')
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

timeout = 10
while not wlan.isconnected() and timeout > 0:
    print("Waiting for router...")
    time.sleep(1)
    timeout -= 1
    
if wlan.isconnected():
    print('Connected!')
    print(wlan.ifconfig())
else:
    print("Error: Could not connect")
