from util_vd import *

# Ensure running as admin - Checzk if the script is already running with administrator privileges
if not ctypes.windll.shell32.IsUserAnAdmin(): # If not, re-run the script with administrator privileges
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit()

displayManager = VirtualDisplayManager()
displayManager.clear()