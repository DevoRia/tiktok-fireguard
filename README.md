# TikTok Fire Guard

This project automates the process of sending messages on TikTok using Python and Selenium.

## Features
- **Manual Login**: Manually log in during the first run to save session cookies for subsequent automations.
- **Automatic Messaging**: Automatically send messages to specified TikTok users.
- **Run Modes**:
  - **Single Mode**: Executes the script once to send a message.
  - **Cron Mode**: Sets up a cron job to run the script daily.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set environment variables:
    - `TARGET_USER`: The TikTok username to whom the message will be sent (default: "Bob").
    - `MESSAGE`: The message to send (default: "Ping").
    - `RUN_MODE`: Defines the mode of script execution. Use:
      - `single` for a one-time execution.
      - `cron` to configure daily execution using a cron job.
    - `PROXY`: Optional HTTP proxy server (e.g. `http://127.0.0.1:8080`). This can also be set via the `--proxy` CLI option.

3. Run the script:
   - **Single Mode** (default):
     ```bash
     RUN_MODE=single TARGET_USER=Alice PROXY=http://127.0.0.1:8080 python main.py
     ```
     Or using the CLI option:
     ```bash
     python main.py --proxy http://127.0.0.1:8080
     ```
   - **Cron Mode**:
     ```bash
     RUN_MODE=cron TARGET_USER=Homie python main.py
     ```

## Cron Job
- When run in **`cron` mode**, the script sets up a daily cron job to execute at 8:00 AM.
- Logs and errors from the cron job are written to `/path/to/your/logfile.log`. Update this path in the script as needed.

## Note
- Chrome WebDriver is required and should match your Chrome version.
- The script requires manual login during the first run to save cookies.