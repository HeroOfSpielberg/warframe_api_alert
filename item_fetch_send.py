import requests
import schedule
import time



def check_invasions():
    url = "https://api.warframestat.us/pc/invasions"  # Change 'pc' to your platform if needed
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        invasions = response.json()
        
        for invasion in invasions:
            # Check attacker rewards
            if 'attackerReward' in invasion and 'countedItems' in invasion['attackerReward']:
                for item in invasion['attackerReward']['countedItems']:
                    if item['type'].lower() == "KarakWraithReceiver":
                        print(f"Found KarakWraithReceiver in attacker rewards: {invasion['node']}")
            
            # Check defender rewards
            if 'defenderReward' in invasion and 'countedItems' in invasion['defenderReward']:
                for item in invasion['defenderReward']['countedItems']:
                    if item['type'].lower() == "KarakWraithReceiver":
                        print(f"Found KarakWraithReceiver in defender rewards: {invasion['node']}")
        
        print("Invasion check completed.")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

# Run the check immediately when the script starts
check_invasions()

# Schedule the check to run every hour
schedule.every().hour.do(check_invasions)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
