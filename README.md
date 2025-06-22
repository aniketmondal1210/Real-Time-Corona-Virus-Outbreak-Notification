🦠 COVID-19 Desktop Tracker (India)

This Python script uses real-time data from the disease.sh API to track COVID-19 statistics for India and specific Indian states. It displays desktop notifications with key updates such as total cases, active cases, recovered, deaths, new deaths, and death rate.

📦 Features

    📊 Monitors India's nationwide COVID-19 stats

    🧭 Tracks selected states: West Bengal, Delhi, Maharashtra, Karnataka, Tamil Nadu

    🚨 Highlights states with the highest cases and deaths

    🖥️ Sends regular desktop notifications

    🔄 Auto-updates every hour (configurable)

🔧 Requirements

    Python 3.x

    Required libraries:

        requests

        plyer

Install dependencies:

pip install requests plyer

🛠️ Setup

    Clone or download the repository.

    (Optional) Place an icon file named icon.ico in the same directory for custom notification icons.

    Run the script:

python covid_tracker.py

⚙️ Configuration

    States to monitor: Change STATES_TO_MONITOR list in the script.

    Notification interval: Change UPDATE_INTERVAL (default is 3600 seconds = 1 hour).

🖼️ Notification Sample

Each notification includes:

    Total cases

    Active cases

    Recovered

    Total deaths

    New deaths

    Death rate

Special symbols:

    ⚠️ = Highest total cases

    💀 = Highest total deaths

📡 Data Source

    API: disease.sh

    Endpoints:

        https://disease.sh/v3/covid-19/countries/india

        https://disease.sh/v3/covid-19/gov/india

🛑 Stop the Script

Press Ctrl + C to safely exit the tracker loop.
📄 License

This project is open-source and available under the MIT License.
