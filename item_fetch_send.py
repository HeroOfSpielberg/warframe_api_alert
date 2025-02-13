#This is a local version that doesn't call the discord webhook and just prints in the console

import requests
import schedule
import time

def check_invasions():
    url = "https://api.warframestat.us/pc/invasions"  # Change 'pc' to your platform if needed
    search_item = "Karak"  # Change this to the item you're looking for (case-insensitive)
    found = False

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        invasions = response.json()

        for invasion in invasions:

            # Function to recursively search for the item in the reward structure
            def search_reward(reward):
                if isinstance(reward, dict):
                    if 'countedItems' in reward:
                        for item in reward['countedItems']:
                            if 'type' in item and search_item.lower() in item['type'].lower():
                                return item['type']  # Return the full item name
                    for key, value in reward.items():
                        if isinstance(value, str) and search_item.lower() in value.lower():
                            return value  # Return the full value found
                        if isinstance(value, list):
                            for i in value:
                                result = search_reward(i)
                                if result:
                                    return result  # Return the found value
                    return None
                elif isinstance(reward, list):
                    for item in reward:
                        result = search_reward(item)
                        if result:
                            return result
                    return None
                return None

            # Check defender rewards
            if 'defender' in invasion and 'reward' in invasion['defender']:
                found_reward = search_reward(invasion['defender']['reward'])
                if found_reward:
                    print(f"Found {found_reward} in defender rewards: {invasion['node']}")
                    found = True

            # Check attacker rewards
            if 'attacker' in invasion and 'reward' in invasion['attacker']:
                found_reward = search_reward(invasion['attacker']['reward'])
                if found_reward:
                    print(f"Found {found_reward} in attacker rewards: {invasion['node']}")
                    found = True

        if not found:
            print(f"{search_item} not found")
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
