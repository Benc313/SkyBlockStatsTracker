# Hypixel Skyblock Stats Tracker

**A personal full-stack web application designed to automatically track and visualize your Hypixel Skyblock player statistics over time.**

This project provides a complete solution from data collection to interactive visualization. It leverages the official Hypixel API to collect player data, stores historical data in a local SQLite database, exposes this data via a Flask API, and presents it through a dynamic React frontend with interactive graphs.

---

## ✨ Features

* **Automated Data Collection:** Periodically collects comprehensive player stats using the official [Hypixel API](https://api.hypixel.net/).
    * Fetches general profile info (Purse, Bank, Kills, Deaths).
    * Detailed Skill and Slayer levels.
    * Comprehensive Bestiary kill counts.
    * All Collections data.
* **Local Data Storage:** All historical data is stored persistently in a lightweight SQLite database (`skyblock_stats.db`).
* **RESTful API (Python Flask):**
    * Provides endpoints to retrieve the latest stats and historical data for graphing.
    * Allows manual triggering of the data collection process.
* **Interactive Web Frontend (React):**
    * **Dashboard:** Overview of latest stats and calculated progress for Collections and Bestiary.
    * **Graphs:** Visualize historical trends for Skills, Profile Stats, Collections, and Bestiary over custom time periods.
* **Containerized Deployment:** Includes a `Dockerfile` for easy containerized deployment.

## 🚀 Technologies Used

**Backend:**
* **Python 3.9+**
* **Flask:** Web framework for the API.
* **Requests:** For making HTTP requests to the Hypixel API.
* **python-dotenv:** For managing environment variables.
* **SQLite3:** Local database for data storage.

**Frontend:**
* **React 18+:** JavaScript library for building the user interface.
* **Tailwind CSS:** For rapid UI development (included via CDN).
* **Recharts:** For rendering interactive historical data graphs.

**Deployment:**
* **Docker:** For containerization of the application.

## 📖 Getting Started

### Prerequisites

* **Python 3.9+**
* **Node.js & npm**
* **A Hypixel API Key:** You can obtain one by logging into the Hypixel server and typing the command `/api new`.

### Local Development Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```

2.  **Backend Setup (Python & Flask API):**
    * **Install Python dependencies:**
        ```bash
        pip install -r requirements.txt
        ```
    * **Create Environment File:**
        Create a file named `.env` in the root of the project and add your Hypixel API key:
        ```
        HYPIXEL_API_KEY=your_api_key_here
        ```
    * **Run the Flask API:**
        Open a terminal and start the Flask API.
        ```bash
        export FLASK_APP=app.py
        flask run --host=0.0.0.0 --port=5000
        ```
        The Flask server will be running on `http://localhost:5000`.

3.  **Frontend Setup (React App):**
    * **Navigate to the frontend directory:**
        ```bash
        cd skyblock-dashboard
        ```
    * **Install Node.js dependencies:**
        ```bash
        npm install
        ```
    * **Start the React development server:**
        ```bash
        npm start
        ```
        This will open the app in your browser at `http://localhost:3000`.

4.  **Perform your first data collection:**
    * **Option 1 (From the App):** Once the frontend is running, click the "Collect Latest Data" button.
    * **Option 2 (Manual Script):** Run the collection script directly.
        ```bash
        python hypixel_tracker.py
        ```
    A `skyblock_stats.db` file will be created in the root directory.

### Deployment with Docker

1.  **Build the Docker image:**
    ```bash
    docker build -t skyblock-tracker .
    ```

2.  **Run the Docker container:**
    This command starts your container, maps the API port, and sets your API key.
    ```bash
    docker run -d \
      -p 5000:5000 \
      -e HYPIXEL_API_KEY="your_api_key_here" \
      --name skyblock-tracker \
      skyblock-tracker
    ```
    * You will need to configure the `skyblock-dashboard/src/App.js` to point to your server's IP address instead of `127.0.0.1`.

## ⚠️ Important Notes

* **API Rate Limiting:** Be mindful of the Hypixel API rate limits. The default limit is typically 120 requests per minute.
* **Not Affiliated:** This project is an independent tool and is not affiliated with Hypixel or Mojang.