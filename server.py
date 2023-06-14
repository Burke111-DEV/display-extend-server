import asyncio
import subprocess
import websockets
import json
from util_vd import *
from util_stream import *
from util_adb import *

# Ensure running as admin - Check if the script is already running with administrator privileges
if not ctypes.windll.shell32.IsUserAnAdmin(): # If not, re-run the script with administrator privileges
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit()

DYNAMIC_BITRATE = True
displayManager = VirtualDisplayManager(_log=False)
streamManager = None
streamProcess = None

# Controls WebSocket server code
async def ctrlsWsOnConnect(_ctrlsWs, path):
    r = json.loads(await _ctrlsWs.recv())

    if not "width" in r:
        return # Bad result
    
    # Create virtual display
    display = displayManager.addDisplay(width = r["width"], height = r["height"] )

    # Stream virtual display
    reverse_port("tcp:8008", "tcp:8008")    # Connect ports for Controls WSS
    streamProcess = runStream(display, (r["width"], r["height"]))
    
    # Ready to start streaming
    await _ctrlsWs.send(json.dumps( { "cmd": "START" } ))

    # Handle incoming msgs
    try:
        while True:
            r = json.loads(await _ctrlsWs.recv())
            if "QUIT" in r["cmd"]:
                displayManager.quit()
                streamProcess.terminate()
                exit()

    except websockets.exceptions.ConnectionClosedError:
        # Handle connection closed error
        print("CLOSED")
        pass

def runStream(display, clientRes):
    script_command = ['python', f'{PROJECT_ROOT}\\stream_server.py', display, json.dumps(clientRes)]
    if DYNAMIC_BITRATE: script_command.append("--dynamic-bitrate")
    venv_activate_cmd = ['cmd', '/k', f"{PROJECT_ROOT}\\env\\Scripts\\activate", '&&']

    return subprocess.Popen(venv_activate_cmd + script_command)
    
def closeStream():
    streamProcess.terminate()
    streamProcess.wait()


# Main execution
if __name__ == '__main__':
    try:
        # Setup controls websocket server
        startCtrlsWss = websockets.serve(ctrlsWsOnConnect, 'localhost', 8000)
        asyncio.get_event_loop().run_until_complete(startCtrlsWss)
        print("Controls WebSocket server started on port 8000.")

        # Get android device
        wait_for_device()                       # Get ADB device
        reverse_port("tcp:8000", "tcp:8000")    # Connect ports for Controls WSS
    except Exception as e:
        print(f"TL Failed: {e}")
    
    asyncio.get_event_loop().run_forever()