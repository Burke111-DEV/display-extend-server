import sys
import json
import asyncio
import websockets
from screeninfo import get_monitors
from util_stream import *
from util_vd import displayJSONToMonitor
import time
import threading

# Acquire display and client resolutions and check if using dynamic bitrate
if not len(sys.argv) > 1: exit()
DISPLAY = displayJSONToMonitor(json.loads(sys.argv[1]))
CLIENTRES = json.loads(sys.argv[2])
DYNAMIC_BITRATE = len(sys.argv) >= 4 and sys.argv[3] == "--dynamic-bitrate"
print(f"STREAMSERVER::display={DISPLAY}:{type(DISPLAY)},resolution={CLIENTRES}:{type(CLIENTRES)},dynamic-bitrate={DYNAMIC_BITRATE}")


event_loop = asyncio.get_event_loop()

# Setup and run capture and websocket stream
async def streamWsOnConnect(_streamWs, _path, _streamManager):
    print("Stream WS Client Connected")
    _streamManager.setWs(_streamWs)
    await _streamManager.stream()

streamManager = StreamManager(DISPLAY.width, DISPLAY.height, CLIENTRES[0], CLIENTRES[1], DISPLAY.x, DISPLAY.y, _dynamicBitrate=DYNAMIC_BITRATE)
startStreamWs = websockets.serve(lambda ws, path: streamWsOnConnect(ws, path, streamManager), 'localhost', 8008)
asyncio.ensure_future(startStreamWs)

# Listen for monitor changes and update stream
def displayConfigCheck():
    initial_monitors = get_monitors()

    while True:
        time.sleep(4)  # Wait for 4 seconds
        updated_monitors = get_monitors()

        if updated_monitors != initial_monitors:
            initial_monitors = updated_monitors
            new_monitor = next((monitor for monitor in updated_monitors if monitor.name == DISPLAY.name), None)
            streamManager.updateDisplay(new_monitor)

displayConfigThread = threading.Thread(target=displayConfigCheck)
displayConfigThread.start()

# Monitor FFMPEG bitrate and adjust stream in realtime.
def bitrateCheck():
    import re
    pattern = r"bitrate=\s*(.*?)\s*bits/s"

    while True:
        time.sleep(2)  # Wait for 4 seconds

        d = streamManager.ffmpegProcess.stderr.read(1024).decode("utf-8")
        bitrate_matches = re.findall(pattern, d)

        if len(bitrate_matches):
            bitrate = bitrate_matches[-1].lstrip()
            b = int(float(bitrate[:-1])*1000/streamManager.FRAMERATE)
            # streamManager.BITRATE = b
            streamManager.BITRATE = int( (streamManager.BITRATE * 0.5) + ( b * 0.5) )   # Smoothing to prevent sudden bitrate spikes
        elif len(d) > 8:
            d = streamManager.ffmpegProcess.stderr.read(4096).decode("utf-8")   # Else, clear buffer out
       
if DYNAMIC_BITRATE:
    statsThread = threading.Thread(target=bitrateCheck)
    statsThread.start()

asyncio.get_event_loop().run_forever()



