import network
from time import sleep

ssid = 'YOUR_WIFI_SSID'  # Replace with your Wi-Fi network name
password = 'YOUR_WIFI_PASSWORD'  # Replace with your Wi-Fi password

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait for connection
while not wlan.isconnected():
    print('Waiting for connection...')
    sleep(1)

print('Connected to', ssid)
print('IP Address:', wlan.ifconfig()[0])
