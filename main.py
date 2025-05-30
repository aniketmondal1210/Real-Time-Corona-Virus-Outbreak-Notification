from plyer import notification
import requests
import time
import os
from datetime import datetime

# API URLs
URL = 'https://disease.sh/v3/covid-19/countries/india'
STATES_URL = 'https://disease.sh/v3/covid-19/gov/india'

# States to monitor
STATES_TO_MONITOR = ['West Bengal', 'Delhi', 'Maharashtra', 'Karnataka', 'Tamil Nadu']

# Time settings (in seconds)
UPDATE_INTERVAL = 3600  # 1 hour
WAIT_BETWEEN_NOTIFICATIONS = 2  # 2 seconds

def send_notification(title, message):
    """Send a desktop notification"""
    try:
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
        notification.notify(
            title=title,
            message=message,
            app_icon=icon_path if os.path.exists(icon_path) else None,
            timeout=10
        )
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Sent: {title}")
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Error sending notification: {e}")

def get_covid_data():
    """Fetch COVID-19 data from API"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/json'
        }

        # Get India's overall data
        india_response = requests.get(URL, headers=headers, timeout=10)
        india_response.raise_for_status()
        india_data = india_response.json()
        
        # Get state-wise data
        states_response = requests.get(STATES_URL, headers=headers, timeout=10)
        states_response.raise_for_status()
        states_data = states_response.json()
        
        return india_data, states_data
    except requests.RequestException as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Error fetching data: {e}")
        return None, None
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Unexpected error: {e}")
        return None, None

def calculate_stats(data):
    """Calculate death rate and format numbers"""
    cases = data.get('cases', 0)
    deaths = data.get('deaths', 0)
    today_deaths = data.get('todayDeaths', 0)
    death_rate = (deaths / cases * 100) if cases > 0 else 0
    
    return {
        'cases': f"{cases:,}",
        'active': f"{data.get('active', 0):,}",
        'recovered': f"{data.get('recovered', 0):,}",
        'deaths': f"{deaths:,}",
        'today_deaths': f"{today_deaths:,}",
        'death_rate': f"{death_rate:.2f}%"
    }

def main():
    """Main function to run the COVID tracker"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] COVID-19 Tracker Started")
    print(f"Monitoring: India, {', '.join(STATES_TO_MONITOR)}, and states with highest cases/deaths")
    
    while True:
        try:
            india_data, states_data = get_covid_data()
            
            if india_data and states_data:
                # Show India's statistics with death details
                india_stats = calculate_stats(india_data)
                send_notification(
                    "🇮🇳 COVID-19 India Update",
                    f"INDIA OVERALL:\n"
                    f"Total Cases: {india_stats['cases']}\n"
                    f"Active Cases: {india_stats['active']}\n"
                    f"Recovered: {india_stats['recovered']}\n"
                    f"⚠️ Total Deaths: {india_stats['deaths']}\n"
                    f"💀 New Deaths: {india_stats['today_deaths']}\n"
                    f"Death Rate: {india_stats['death_rate']}"
                )
                time.sleep(WAIT_BETWEEN_NOTIFICATIONS)
                
                # Process state data
                all_states = states_data.get('states', [])
                
                # Find states with highest cases and deaths
                highest_cases = max(all_states, key=lambda x: x.get('cases', 0))
                highest_deaths = max(all_states, key=lambda x: x.get('deaths', 0))
                
                # Track states to show (monitored + highest cases/deaths)
                states_to_show = []
                for state in all_states:
                    state_name = state['state']
                    if (state_name in STATES_TO_MONITOR or 
                        state == highest_cases or 
                        state == highest_deaths):
                        if state not in states_to_show:  # Avoid duplicates
                            states_to_show.append(state)
                
                # Show notifications for selected states with death details
                for state in states_to_show:
                    state_stats = calculate_stats(state)
                    
                    # Prepare title with indicators
                    title = f"📊 COVID-19: {state['state']}"
                    if state == highest_cases:
                        title += " ⚠️ Highest Cases"
                    if state == highest_deaths:
                        title += " 💀 Highest Deaths"
                    
                    send_notification(
                        title,
                        f"STATE: {state['state'].upper()}\n"
                        f"Total Cases: {state_stats['cases']}\n"
                        f"Active Cases: {state_stats['active']}\n"
                        f"Recovered: {state_stats['recovered']}\n"
                        f"⚠️ Total Deaths: {state_stats['deaths']}\n"
                        f"💀 New Deaths: {state_stats['today_deaths']}\n"
                        f"Death Rate: {state_stats['death_rate']}"
                    )
                    time.sleep(WAIT_BETWEEN_NOTIFICATIONS)
            
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Next update in 1 hour...")
                time.sleep(UPDATE_INTERVAL)
            
        except KeyboardInterrupt:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Stopping COVID tracker...")
            break
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Error: {e}")
            print("Retrying in 1 minute...")
            time.sleep(60)

if __name__ == "__main__":
    main()