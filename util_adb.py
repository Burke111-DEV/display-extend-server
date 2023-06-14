import time
import subprocess

def get_root_folder_path():
    wd = subprocess.run('cd', shell=True, capture_output=True, text=True).stdout.strip()
    split_index = wd.find(PROJECT_FOLDER_NAME)
    if split_index != -1: 
        ROOT = wd[:split_index + len(PROJECT_FOLDER_NAME)]
    return ROOT
PROJECT_FOLDER_NAME = "display-extend-server"
PROJECT_ROOT = get_root_folder_path()
ADB_LOC = f'{PROJECT_ROOT}\\bin\\platform-tools\\adb.exe'

# ADB command execution using subprocess
def run_adb_command(command):
    process = subprocess.Popen([ADB_LOC] + command, stdout=subprocess.PIPE)
    output, _ = process.communicate()
    return output.decode().strip()

# Check for connected Android devices using ADB
def check_for_devices():
    output = run_adb_command(['devices'])
    lines = output.split('\n')[1:]
    devices = [line.split('\t')[0] for line in lines if line.strip() != '']
    return devices

# Wait for an Android device to appear
def wait_for_device():
    i = 0
    while True:
        devices = check_for_devices()
        if devices:
            print(f"Got Device: {devices}")
            break
        else:
            print("No devices found. Waiting.." + (". " if i%2==0 else "  "), end="\r")
            i += 1
            time.sleep(2)
    return devices

# Forward local port 8008 to the Android device
def reverse_port(local="tcp:9000", remote="tcp:8000"):
    run_adb_command(['reverse', local, remote])
    print(f"Reverse Port Forward: {local} : {remote}")