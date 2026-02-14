# Silent Emergency Button (Safety Assistant)

A web-based silent emergency alert system designed to send immediate distress signals with location data to a trusted contact.

## Features
- **One-Tap SOS**: A large, easy-to-hit button to trigger an alert.
- **Silent Operation**: Designed to be discreet.
- **Location Tracking**: Automatically captures the device's GPS coordinates (`latitude`, `longitude`).
- **Email Alerts**: Sends an email to a pre-configured trusted contact with a Google Maps link.
- **Visual Feedback**: Provides clear "SENDING..." and "SENT" status on the button.


## Prerequisites
- **Python 3.x**: Ensure Python is installed on your system.
- **pip**: Python package manager.

## Installation

1.  **Clone or Download** the project repository.
2.  **Navigate** to the project directory:
    ```bash
    cd path/to/emergency
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *Dependencies include: `Flask`, `Flask-Mail`, `requests`.*

## Configuration (Email)

To enable email sending, you must configure environment variables for your email provider (e.g., Gmail).
You can set these in your terminal session or add them to a `.env` file (if you use `python-dotenv`, not included by default).

**Example (Windows PowerShell):**
```powershell
$env:MAIL_USERNAME = "your-email@gmail.com"
$env:MAIL_PASSWORD = "your-app-password" # Use an App Password, not your login password!
```

**Default Config:**
- Server: `smtp.googlemail.com`
- Port: `587`
- TLS: `Enabled`

## Usage

1.  **Start the Server**:
    Run the following command in your terminal:
    ```bash
    python app.py
    ```
    You should see output indicating the server is running on `http://127.0.0.1:5000`.

2.  **Access the Application**:
    Open your web browser and go to:
    **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

    > [!IMPORTANT]
    > **Do NOT open `index.html` directly** by double-clicking it. The app requires the backend server to function. If you open the file directly, you will see a critical error alert.

3.  **Trigger an Alert**:
    - Enter a **Trusted Contact** email/phone (optional, saved locally).
    - Click the **SOS** button.
    - Allow **Location Access** if prompted.
    - The button will turn green and say **SENT** upon success.

## Troubleshooting

-   **"Error: NetworkError" / "Failed to fetch"**:
    -   Ensure the backend server is running (`python app.py`).
    -   Ensure you are accessing via `http://127.0.0.1:5000`.

-   **"Geolocation is not supported"**:
    -   Ensure you are using a modern browser.
    -   Note: Some browsers restrict Geolocation on insecure origins (HTTP), but `localhost` is usually treated as a secure context.

-   **Email not sending**:
    -   Check your `MAIL_USERNAME` and `MAIL_PASSWORD` environment variables.
    -   Check the server console output for specific SMTP errors.

## Project Structure
-   `app.py`: Flask backend server handling API requests.
-   `index.html`: Main user interface.
-   `static/style.css`: Styling for the application (Dark Mode).
-   `static/script.js`: Frontend logic for button clicks, location, and API calls.
-   `test_alert.py`: Script to manually test the complete backend flow.
