import os
import sys
import subprocess
import ctypes
from ctypes import wintypes
from screeninfo import get_monitors, Monitor
import json

def getDisplayDetails():
    displayData = []
    monitors = get_monitors()
    for monitor in monitors:
        displayData.append(monitor)
    return displayData

def driverSetup():
    os.chdir("bin/usbmmidd_v2")
    subprocess.run("deviceinstaller64 install usbmmidd.inf usbmmidd", shell=True)

def setResolutions(width, height):
    # Swap so height is always smallest, and scale height to 768 which is minimum allowable
    if height > width: height, width = width, height
    width =  int(round(width * (768 / height)))
    height = 768

    addResolution = r'reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\WUDF\Services\usbmmIdd\Parameters\Monitors" '
    addResolutionFull= addResolution + f'/t REG_SZ /d "{width},{height}" /f'
    subprocess.call(addResolutionFull, shell=True)
    
    for i in range(0, 9):
        addResolutionFull= addResolution + f'/v "{i}" /t REG_SZ /d "{width},{height}" /f'
        subprocess.call(addResolutionFull, shell=True)

def createDisplay():
    subprocess.run("deviceinstaller64 enableidd 1", shell=True)

def removeDisplay():
    subprocess.run("deviceinstaller64 enableidd 0", shell=True)

def closeDriver():
    subprocess.run("deviceinstaller64 stop usbmmidd", shell=True)
    subprocess.run("deviceinstaller64 remove usbmmidd", shell=True)

def displayJSON(display):
    return json.dumps({
        "x": display.x,
        "y": display.y,
        "width": display.width,
        "height": display.height,
        "width_mm": display.width_mm,
        "height_mm": display.height_mm,
        "name": display.name,
        "is_primary": display.is_primary
    })

def displayJSONToMonitor(display):
    return Monitor(
        x=display["x"],
        y=display["y"],
        width=display["width"],
        height=display["height"],
        width_mm=display["width_mm"],
        height_mm=display["height_mm"],
        name=display["name"],
        is_primary=display["is_primary"]
    )

class VirtualDisplayManager:
    def __init__(self, _log=True):
        self.displayDetails = getDisplayDetails()
        self.virtualDisplays = {}
        self.ended = False
        self.log = _log
        driverSetup()
    
    def addDisplay(self, width=1920, height=1080):
        setResolutions(height, width)
        createDisplay()
        
        # Add any new displays to the list of virtual displays
        latestDetails = getDisplayDetails()
        newDisplays = [item for item in latestDetails if item not in self.displayDetails]
        self.displayDetails = latestDetails
        
        newDisplayName = newDisplays[-1].name.split('\\')[-1]
        self.virtualDisplays[newDisplayName] = newDisplays[-1]

        if(self.log): print(f'Added Display: {newDisplayName}')
        return displayJSON(self.virtualDisplays[newDisplayName])

    def clear(self):
        if len(self.displayDetails) >1 : 
            for i in range(len(self.displayDetails)-1):
                removeDisplay()
        closeDriver()
    
    def quit(self):
        if(not self.ended):
            if self.log: print("EXITING")
            for i in range(len(self.virtualDisplays)):
                removeDisplay()
            closeDriver()
            self.ended = True