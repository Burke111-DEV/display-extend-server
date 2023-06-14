# Project Setup

## 1. Install Python dependencies

- Recommended: Create a pip virtual environment with the following commands:
    ```
    python -m venv env
    env\Scripts\activate
    ```

- Install dependencies by running the command:
    ```
    pip install -r req.txt
    ```

- Note: If you encounter errors related to pywin32, run the following command:
    ```
    cd env
    python Scripts/pywin32_postinstall.py -install
    ```

## 2. Gather Tools

- Run the gather script to assemble the `bin` folder containing ffmpeg, Android platform-tools, and Amyuni's virtual display drivers. Execute the following command:
    ```
    python .\gather_tools.py
    ```

## 3. Run the Server (Run as administrator)

- Start the server by running the command:
    ```
    python .\server.py
    ```

## 4. Connect Client Android device via USB and open DisplayExtend client app.

## 5. Additional display should be added. Enjoy.

- If nothing happens after opening the app, try pressing the Enter key in the shell window as it occasionally freezes.

- Only connect one Android device via USB at a time.

- Ensure the server is running before connecting the client and opening the app.

## 6. Exit

- Simply close the window running the server.py script.

- Finally, clear out the virtual display by running the cleanup script.
    ```
    python .\cleanup.py
    ```
