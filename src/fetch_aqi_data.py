import json
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv


project_root = Path(__file__).resolve().parent.parent
env_file = project_root / ".env"

load_dotenv(env_file)

api_key = os.getenv("DATA_GOV_API_KEY")

if not api_key:
    raise ValueError("DATA_GOV_API_KEY was not found")


api_url = (
    "https://api.data.gov.in/resource/"
    "3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69"
)

params = {
    "api-key": api_key,
    "format": "json",
    "filters[state]": "Telangana",
    "filters[city]": "Hyderabad",
    "offset": 0,
    "limit": 5,
}

max_attempts = 3

response = None


for attempt in range(1, max_attempts + 1):
    print(f"API request attempt {attempt}/{max_attempts}")

    try:
        response = requests.get(
            api_url,
            params=params,
            timeout=60,
        )

        response.raise_for_status()

        print("API request successful")
        break

    except requests.exceptions.Timeout:
        print("API request timed out")

        if attempt < max_attempts:
            print("Waiting 5 seconds before retrying...")
            time.sleep(5)

    except requests.exceptions.RequestException as error:
        print(f"API request failed: {error}")
        break


if response is None or not response.ok:
    raise RuntimeError(
        "Unable to retrieve AQI data from the official API"
    )


data = response.json()


print("\nCityPulse Hyderabad - Official AQI API Inspection")
print("-" * 55)

print(f"HTTP status: {response.status_code}")
print(f"Response type: {type(data).__name__}")

print("\nTop-level JSON keys:")
print(list(data.keys()))

print("\nTotal records reported by API:")
print(data.get("total"))

records = data.get("records", [])

print("\nRecords received in this request:")
print(len(records))

if records:
    print("\nFirst official AQI record:")
    print(json.dumps(records[0], indent=2))