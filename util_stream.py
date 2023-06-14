
import subprocess

def get_root_folder_path():
    wd = subprocess.run('cd', shell=True, capture_output=True, text=True).stdout.strip()
    split_index = wd.find(PROJECT_FOLDER_NAME)
    if split_index != -1: 
        ROOT = wd[:split_index + len(PROJECT_FOLDER_NAME)]
    return ROOT
PROJECT_FOLDER_NAME = "display-extend-server"
PROJECT_ROOT = get_root_folder_path()
FFMPEG_LOC = f'{PROJECT_ROOT}\\bin\\ffmpeg\\bin\\ffmpeg.exe'

class StreamManager:
    def __init__(self, _width, _height, _originaWidth, _originalHeight, _x, _y, _framerate=30, _log=True, _dynamicBitrate=True):
        self.log = _log
        self.DB = _dynamicBitrate
        self.WIDTH = int((_width // 2) * 2)     # ffmpeg asks for multiple of 2
        self.HEIGHT = int((_height // 2) * 2)
        self.ORIGINAL_WIDTH =  int((_originaWidth   // 2) *2)
        self.ORIGINAL_HEIGHT = int((_originalHeight // 2) *2)
        self.X = int((_x // 2) * 2)
        self.Y = int((_y // 2) * 2)
        self.FRAMERATE = _framerate
        self.BITRATE = int(_originaWidth * _originalHeight*32)
        self.pauseFfmpeg = False

        self.ffmpegCmd = [
            FFMPEG_LOC,
                '-f', 'gdigrab',
                '-framerate', f'{self.FRAMERATE}',
                '-i', 'desktop',
                '-filter:v', f"crop={self.WIDTH}:{self.HEIGHT}:{self.X}:{self.Y}",
                '-c:v', 'libx264',
                '-preset', 'ultrafast',
                '-tune', 'zerolatency',
                '-pix_fmt', 'yuv420p',
                '-profile:v', 'baseline',
                '-level', '6.2',
                '-f', 'rawvideo',
                '-hide_banner',
                '-stats', 
                '-'
            ]
        self.ffmpegProcess = None
    

    def updateFfmpegCommand(self, _framerate=None, _preset=None, _w=None, _h=None, _x=None, _y=None, _ogW=None, _ogH=None):
        if isinstance(_framerate, str) or isinstance(_framerate, int):
            idx = self.ffmpegCmd.index("-framerate")+1
            self.ffmpegCmd[idx] = _framerate

        if isinstance(_preset, str):
            idx = self.ffmpegCmd.index("-preset")+1
            self.ffmpegCmd[idx] = _preset

        if (isinstance(_w, str) or isinstance(_w, int)) and (isinstance(_h, str) or isinstance(_h, int)) and (isinstance(_x, str) or isinstance(_x, int)) and (isinstance(_y, str) or isinstance(_y, int)):
            idx = self.ffmpegCmd.index("-filter:v")+1
            filterSplit = self.ffmpegCmd[idx].split(",")
            self.ffmpegCmd[idx] = f"{f'crop={_w}:{_h}:{_x}:{_y}'},{filterSplit[-1]}"

        if (isinstance(_ogW, str) or isinstance(_ogW, int)) and (isinstance(_ogH, str) or isinstance(_ogH, int)):
            idx = self.ffmpegCmd.index("-filter:v")+1
            filterSplit = self.ffmpegCmd[idx].split(",")
            self.ffmpegCmd[idx] = f"{filterSplit[0]},{f'scale={_ogW}:{_ogH}'}"
    
    def runFfmpeg(self):
        if self.ffmpegProcess: return       # Cancel if already has process
        if self.log: print(self.ffmpegCmd)

        try:
            self.ffmpegProcess = subprocess.Popen(self.ffmpegCmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0)
            self.pauseFfmpeg = False
        except Exception as e:
            print(f"Failed to run ffmpeg: {e}")
    
    def cancelFfmpeg(self):
        if not self.ffmpegProcess: return   # Cancel if no running process

        try:
            self.pauseFfmpeg = True
            self.ffmpegProcess.terminate() # Kill signal
            self.ffmpegProcess.wait()      # Wait for completion
            self.ffmpegProcess = None
        except Exception as e:
            print(f"Failed to cancel ffmpeg: {e}")

    def restartFfmpeg(self):
        if self.ffmpegProcess:
            self.cancelFfmpeg()
        self.runFfmpeg()

    def setWs(self, _ws):
        self.ws = _ws

    async def stream(self):
        if not self.ffmpegProcess:
            self.runFfmpeg()

        try:
            if(self.log): print("Stream Running...")
            while True:
                if not self.ffmpegProcess: continue
                frameData = self.ffmpegProcess.stdout.read(self.BITRATE)
                if not frameData and not self.pauseFfmpeg: 
                    break
                await self.ws.send(frameData)
        finally:
            if(self.log): print("Stream Ended.")
            self.cancelFfmpeg()
                
    def updateDisplay(self, display):
        self.updateFfmpegCommand(_w=display.width, _h=display.height, _x=display.x, _y=display.y)
        self.restartFfmpeg()

    def quit(self):
        self.cancelFfmpeg()