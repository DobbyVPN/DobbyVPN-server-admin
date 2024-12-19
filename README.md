# Outline Admin Interface

**Outline Admin Interface** provides a user-friendly interface for managing Outline VPN keys. The application features an intuitive terminal-based interface built using the Textual library.

## Features

- **View All Outline VPN Keys:** Easily browse through all existing VPN keys.
- **Add New Keys:** Generate and add new Outline VPN keys seamlessly.
- **Delete Existing Keys:** Remove outdated or unnecessary VPN keys with ease.
- **Rename Keys:** Customize the names of your VPN keys for better organization.
- **Update Keys from Outline Server:** Keep your VPN keys up-to-date by syncing with the Outline server.
- **Manage Environment Variables via `.env` File:** Efficiently handle environment configurations through a simple `.env` file.

## Important!!!
**That's the example of .env file**
   ```bash
    {Json="apiUrl":"...","certSha256":"..."}
   ```



## Installation

### Prerequisites

- **Python 3.8 or higher**
- **pip** (Python package installer)

### Installation Steps

1. **Clone the Repository or Download the Source Code Archive:**

    ```bash
    git clone https://github.com/xaeliudzyh/Outline-Admin-TUI.git
    ```

2. **Navigate to the Project Directory:**

    ```bash
    cd Outline-Admin-TUI
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **After Successfully Installing Dependencies, Run the Application with the Following Command:**

    ```bash
    python main.py
    ```
