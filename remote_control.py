import network
import socket
import machine
from time import sleep
import secrets  # Assumes you have secrets.py with SSID and PASSWORD

# Initialize LED on GP15
led = machine.Pin(15, machine.Pin.OUT)
led.value(0)  # Start with LED off

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.SSID, secrets.PASSWORD)

while not wlan.isconnected():
    print('Waiting for connection...')
    sleep(1)

ip = wlan.ifconfig()[0]
print(f'Connected to Wi-Fi. IP Address: {ip}')

# Simple HTML page to control LED
html = """<!DOCTYPE html>
<html>
<head><title>Pico W LED Control</title></head>
<body>
    <h1>Pico W LED Control</h1>
    <p>LED State: {state}</p>
    <p><a href="/led/on"><button>Turn LED On</button></a></p>
    <p><a href="/led/off"><button>Turn LED Off</button></a></p>
</body>
</html>
"""

# Set up socket server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('Web server running on http://', ip, ':80')

while True:
    try:
        cl, addr = s.accept()
        print('Client connected from', addr)
        request = cl.recv(1024).decode()
        
        # Parse request
        if 'GET /led/on' in request:
            led.value(1)
            state = 'ON'
        elif 'GET /led/off' in request:
            led.value(0)
            state = 'OFF'
        else:
            state = 'ON' if led.value() else 'OFF'

        # Send HTML response
        response = html.format(state=state)
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()

    except OSError as e:
        cl.close()
        print('Connection closed:', e)
