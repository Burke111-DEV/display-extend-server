import os
import shutil
import zipfile
import requests

def download_file(url, destination):
    response = requests.get(url, stream=True)
    with open(destination, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)

def extract_zip(zip_path, destination):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(destination)

def find_matching_folder(folder_path, keywords):
    for folder_name in os.listdir(folder_path):
        if all(keyword in folder_name for keyword in keywords):
            full_path = os.path.join(folder_path, folder_name)
            if os.path.isdir(full_path):
                return full_path
    return None


# Create the "bin" folder if it doesn't exist
bin_folder = "bin"
if not os.path.exists(bin_folder):
    os.makedirs(bin_folder)

# Download and extract usbmm_drivers.zip
# Originally found here: https://www.amyuni.com/forum/viewtopic.php?t=3030
print("  Gathering Amyuni's Virtual Display Drivers...", end="\r")
usbmm_url = "https://www.amyuni.com/downloads/usbmmidd_v2.zip"
usbmm_zip = os.path.join(bin_folder, "usbmm_drivers.zip")
download_file(usbmm_url, usbmm_zip)
extract_zip(usbmm_zip, bin_folder)
usbmm_folder = os.path.join(bin_folder, "usbmmidd_v2")
print("Completed: usbmmidd_v2                                        ")

# Download and extract ffmpeg
# Originally found here: https://www.gyan.dev/ffmpeg/builds/
print("  Gathering ffmpeg for Windows...", end="\r")
ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
ffmpeg_zip = os.path.join(bin_folder, "ffmpeg.zip")
download_file(ffmpeg_url, ffmpeg_zip)
extract_zip(ffmpeg_zip, bin_folder)
ffmpeg_folder = find_matching_folder(bin_folder, ["ffmpeg", "essentials"])
if ffmpeg_folder is not None:
    os.rename(ffmpeg_folder, os.path.join(bin_folder, "ffmpeg"))
print("Completed: ffmpeg                                        ")


# Download and extract android-sdk
# Originally found here: https://developer.android.com/tools/releases/platform-tools
print("  Gathering Android Platform Tools...", end="\r")
sdk_url = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
sdk_zip = os.path.join(bin_folder, "android-sdk.zip")
download_file(sdk_url, sdk_zip)
extract_zip(sdk_zip, bin_folder)
platform_tools_folder = os.path.join(bin_folder, "platform-tools")
print("Completed: Android platform-tools                                        ")

# Clean up the downloaded zip files
os.remove(usbmm_zip)
os.remove(ffmpeg_zip)
os.remove(sdk_zip)
print("Cleaned up archives")

print("Files downloaded and configured successfully.")