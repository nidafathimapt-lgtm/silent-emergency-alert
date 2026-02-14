import requests
import json

# URL of the local server
url = 'http://127.0.0.1:5000/alert'

# Test Data
payload = {
    "latitude": 37.7749,
    "longitude": -122.4194,
    "message": "TEST EMERGENCY ALERT - PLEASE IGNORE",
    "trusted_contact": "test_recipient@example.com" # Change this to your email to test receiving it
}

headers = {
    'Content-Type': 'application/json'
}

print(f"Sending alert to {url}...")
print(f"Payload: {json.dumps(payload, indent=2)}")

try:
    response = requests.post(url, json=payload, headers=headers)
    
    print("\nResponse Status Code:", response.status_code)
    try:
        print("Response JSON:", response.json())
    except:
        print("Response Text:", response.text)
        
    if response.status_code == 200:
        print("\n[OK] Alert Sent Successfully!")
    else:
        print("\n[ERROR] Failed to send alert.")

except requests.exceptions.ConnectionError:
    print("\n[ERROR] Could not connect to the server. Is it running?")
except Exception as e:
    print(f"\n[ERROR] Start Error: {e}")
