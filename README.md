# Hypixel Skyblock Stats Tracker

**A personal full-stack web application designed to automatically track and visualize your Hypixel Skyblock player statistics over time.**

This project provides a complete solution from data collection to interactive visualization. It leverages web scraping with a headless browser, stores historical data in a local SQLite database, exposes this data via a Flask API, and presents it through a dynamic React frontend with interactive graphs and detailed item views. Designed for easy deployment using Docker, it encapsulates the entire backend service, including automated daily scrapes via cron.

---

## ✨ Features

* **Automated Data Scraping:** Daily collection of comprehensive player stats from [SkyCrypt (sky.shiiyu.moe)](https://sky.shiiyu.moe/).
    * Scrapes general player info (Skyblock Level, Networth, Purse, Bank).
    * Detailed Skill and Slayer levels.
    * Comprehensive Bestiary kill counts.
    * All Collections data (by category and individual item amounts).
    * Inventory (visible items), Armor, Weapons, Accessories, and Pets.
    * Dungeons, Minions, Crimson Isle, Rift, and other miscellaneous stats.
    * Utilizes Playwright for robust scraping of dynamically loaded content (scrolls to load all data).
* **Local Data Storage:** All historical data is stored persistently in a lightweight SQLite database.
* **RESTful API (Python Flask):**
    * Provides endpoints to retrieve the latest stats.
    * Serves historical data for graphing with customizable timeframes.
    * Offers dedicated endpoints for gear and item lists.
    * Allows manual triggering of the data scrape for immediate updates.
* **Interactive Web Frontend (React):**
    * **Dashboard:** Overview of latest stats and calculated changes (increases in Bestiary, Collections, core stats) since the last day and last month.
    * **Graphs:** Visualize historical trends for selected stats (e.g., Networth, Skill Average) over custom time periods.
    * **Gear & Items:** Browse your current Armor, Weapons, Accessories, Pets, and Inventory items.
* **Containerized Deployment:** Designed for easy deployment using Docker, running the scraper (via cron) and Flask API concurrently within a single container for isolation and portability.

## 🚀 Technologies Used

**Backend:**
* **Python 3.9+**
* **Flask:** Web framework for the API.
* **Requests:** For HTTP requests.
* **BeautifulSoup4:** For parsing HTML.
* **Playwright:** Headless browser automation for dynamic content scraping.
* **SQLite3:** Local database for data storage.
* **Supervisord:** Process control system to manage Flask API and Cron within Docker.
* **Cron:** For scheduling daily scrapes inside the Docker container.

**Frontend:**
* **React 18+:** JavaScript library for building the user interface.
* **Tailwind CSS:** For rapid UI development and responsive design (included via CDN for simplicity).
* **Recharts:** For rendering interactive historical data graphs.

**Deployment:**
* **Docker:** For containerization of the entire backend service.
* **Ubuntu Server:** Target deployment environment.

## Getting Started

These instructions will get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following installed:

* **Python 3.9+** ([Download Python](https://www.python.org/downloads/))
* **Node.js & npm** (or Yarn) ([Download Node.js](https://nodejs.org/en/download/)) - Node.js comes with npm.
* **Docker Desktop** ([Download Docker Desktop](https://www.docker.com/products/docker-desktop)) - For local testing of the Docker container, or just Docker Engine for server deployment.

### Local Development Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/skyblock-tracker.git](https://github.com/YOUR_USERNAME/skyblock-tracker.git)
    cd skyblock-tracker
    ```

2.  **Backend Setup (Python & Flask API):**
    * **Install Python dependencies:**
        ```bash
        pip install -r requirements.txt
        ```
    * **Install Playwright browser binaries:**
        Playwright needs to download the actual browser engines it controls.
        ```bash
        playwright install
        ```
    * **Run the Flask API:**
        Open a new terminal window/tab in the `skyblock-tracker` directory and start the Flask API.
        ```bash
        export FLASK_APP=api.py # Set FLASK_APP environment variable
        flask run --host=0.0.0.0 --port=5000
        ```
        You should see output indicating the Flask server is running on `http://0.0.0.0:5000`. Keep this terminal running for the frontend to connect.

3.  **Frontend Setup (React App):**
    * **Navigate to the frontend directory:**
        ```bash
        cd frontend
        ```
    * **Install Node.js dependencies:**
        ```bash
        npm install # or yarn install
        ```
    * **Start the React development server:**
        ```bash
        npm start # or yarn start
        ```
        This will open your React app in your browser (usually `http://localhost:3000`).

4.  **Perform your first data scrape (Manual):**
    Since you're starting with an empty database, trigger an initial scrape to populate data.
    You can do this directly from the React frontend by clicking the "Manual Scrape & Save" button, or using `curl` while your Flask API is running:
    ```bash
    # Open another terminal window/tab (not the one running Flask or React)
    curl -X POST http://localhost:5000/api/scrape -H "Content-Type: application/json" -d '{"playerName": "baggett", "profileName": "Papaya"}'
    ```
    Monitor the Flask API terminal for scrape progress. A `skyblock_stats.db` file will be created in your `skyblock-tracker` directory.

### Deployment (Docker on Ubuntu Server)

This section details how to deploy the entire backend (scraper, API, database) within a single Docker container on an Ubuntu server.

1.  **Ensure Docker is installed on your Ubuntu server.**
    Follow the [official Docker documentation](https://docs.docker.com/engine/install/ubuntu/) if you haven't already.

2.  **Transfer project files to your server:**
    Use `git clone` or `scp` to get your `skyblock-tracker` project directory onto your Ubuntu server.
    ```bash
    # On your PC, from the parent directory of skyblock-tracker:
    scp -r skyblock-tracker your_username@your_server_ip:~
    # Then SSH into your server:
    ssh your_username@your_server_ip
    cd skyblock-tracker
    ```

3.  **Create a persistent data volume directory on the host:**
    This directory on your server will store the SQLite database, ensuring your data persists even if the Docker container is removed or updated.
    ```bash
    mkdir -p /home/youruser/skyblock_data_volume # Replace 'youruser' with your actual Ubuntu username
    ```

4.  **Build the Docker image on the server:**
    Navigate to the `skyblock-tracker` directory on your server and build the image. This will download base images, install dependencies, and Playwright browsers. This step may take a while.
    ```bash
    docker build -t skyblock-full-app:latest .
    ```

5.  **Run the Docker container:**
    This command starts your container, maps the API port, and mounts the persistent volume.
    ```bash
    docker run -d \
      -p 5000:5000 \
      -v /home/youruser/skyblock_data_volume:/app/data \
      --name skyblock-tracker \
      skyblock-full-app:latest
    ```
    * `-d`: Runs the container in detached mode (background).
    * `-p 5000:5000`: Maps port 5000 inside the container (where Flask runs) to port 5000 on your Ubuntu host.
    * `-v /home/youruser/skyblock_data_volume:/app/data`: Mounts your host's persistent data directory to `/app/data` inside the container.
    * `--name skyblock-tracker`: Assigns a name to your running container.

6.  **Verify container status and access logs:**
    * Check if running: `docker ps`
    * View Flask API logs: `docker logs -f skyblock-tracker`
    * View Scraper logs (after 5:00 AM UTC): `docker exec skyblock-tracker cat /var/log/skyblock_scraper.log`

7.  **Update Frontend API URL and Deploy Frontend:**
    * On your local machine, open `frontend/src/App.js` and change `API_BASE_URL` to your Ubuntu server's public IP address or domain name:
        ```javascript
        const API_BASE_URL = 'http://YOUR_UBUNTU_SERVER_IP:5000/api';
        ```
    * Build your React frontend for production:
        ```bash
        cd frontend
        npm run build # or yarn build
        ```
    * The `build` folder contains all the static HTML, CSS, and JavaScript for your frontend. You can then transfer this `build` folder to your Ubuntu server and serve it using a web server like Nginx or Apache, or simply use a basic Python HTTP server for testing.

## Usage

Once the backend is running and your frontend is deployed, navigate to your frontend URL (e.g., `http://localhost:3000` for local dev, or `http://your_server_ip` if serving the `build` folder).

* **Dashboard:** See your current stats and recent changes.
* **Graphs:** Select a stat and a timeframe to view its historical progression.
* **Gear & Items:** Explore your collected equipment and inventory items.
* **Manual Scrape:** Click the button to force an immediate update of your stats.

## Important Notes & Disclaimer

* **HTML Structure Changes:** Web scraping relies heavily on the target website's HTML structure. If SkyCrypt changes its layout or class names, the scraper may break and require updates.
* **Rate Limiting:** Be mindful of making too many requests to SkyCrypt. The daily automated scrape is designed to be respectful, but excessive manual scrapes could lead to temporary IP blocks.
* **Not Affiliated:** This project is an independent tool and is not affiliated with Hypixel, Mojang, or SkyCrypt (shiiyu.moe).

## Contributing

Feel free to open issues, submit pull requests, or suggest improvements!

## License

This project is open-source and available under the [MIT License](LICENSE)
