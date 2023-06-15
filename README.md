# Display Extend Server

The Display Extend Server is a Python-based server program that enables you to extend your computer screen to an Android device over USB. This server program works in conjunction with the Display Extend Android Client application, allowing you to utilize your Android device as an additional display.

## Usage

Follow the instructions below to set up and run the Display Extend Server:

1. Install Python dependencies:
    - It is recommended to create a pip virtual environment for the project:
        - Create a virtual environment: 
            - `python -m venv env`
        - Activate the virtual environment:
            - `env\Scripts\activate     # Windows`
            - `source env/bin/activate  # macOS/Linux`
    - Install the project dependencies:
        - `pip install -r req.txt`
    - Note: If you encounter errors related to pywin32, run the following commands from the virtual environment:
        - `cd env`
        - `python Scripts/pywin32_postinstall.py -install`

2. Gather Tools:
    - Run the gather script to assemble the `bin` folder, which contains ffmpeg, Android platform-tools, and Amyuni's virtual display drivers:
        - `python gather_tools.py`

3. Run the Server (Allow run as admin):
    - Launch the Display Extend Server by running the following command:
        - `python server.py`
    - Note: Make sure to run the server with administrative privileges if required by your system.

4. Connect the Client Android Device via USB and Open the DisplayExtend Client App.
    - See the [Android Client project here](https://github.com/Burke111-DEV/display-extend-client-android).

5. Additional Display Setup:
    - Once the server is running, open the Display Extend Android Client app on your Android device.
    - Connect your Android device to the computer via USB.
    - An additional display should be automatically added to your computer.
    - Enjoy using your Android device as an extended display!
    - If nothing happens after opening the app, try pressing the Enter key in the server's shell window as it occasionally freezes.
    - Note: Only connect one Android device via USB at a time.
    - Ensure that the server is running before connecting the client and opening the app.

6. Exiting the Server:
    - Simply close the window running the server.py script.
    - To clear out the virtual display, run the cleanup script:
        - `python cleanup.py`

## Contributing

Contributions to the Display Extend Server project are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

The Display Extend Server project acknowledges the following tools and libraries:

- [Amyuni Virtual Monitor Drivers](https://www.amyuni.com/): Acknowledgements to Amyuni for their virtual monitor drivers, which are utilized in the server program to extend the computer screen to the Android device.

- [FFmpeg](https://ffmpeg.org/): Acknowledgements to FFmpeg for providing the screen capture functionality used in the server program. FFmpeg is a powerful multimedia framework that enables video and audio processing.

- [Android SDK Platform-Tools](https://developer.android.com/studio/releases/platform-tools): Acknowledgements to the Android SDK Platform-Tools, which are included in the server program's `bin` folder and used for various development and debugging tasks, such as device communication and adb commands.

- [ws-avc-player](https://github.com/matijagaspar/ws-avc-player) Library used on the client side to receive and render h264 frame data. It provides valuable functionality for efficient video playback and enhances the overall performance of the client application.

Please note that the Display Extend Server project does not claim ownership or endorse these tools directly.
