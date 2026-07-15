import os
from pathlib import Path

import requests
from dotenv import load_dotenv


project_root = Path(__file__).resolve().parent.parent
load_dotenv(project_root / ".env")

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
    "limit": 1,
}


print("Testing official AQI API")
print("-" * 40)

print("API key exists:", bool(api_key))
print("Sending one-record request...")


try:
    response = requests.get(
        api_url,
        params=params,
        timeout=(10, 20),
    )

    print("Server responded")
    print("HTTP status:", response.status_code)
    print("Content type:", response.headers.get("content-type"))
    print("Response size:", len(response.content))

    print("\nFirst 300 response characters:")
    print(response.text[:300])

except requests.exceptions.ConnectTimeout:
    print("RESULT: CONNECTION TIMEOUT")

except requests.exceptions.ReadTimeout:
    print("RESULT: READ TIMEOUT")

except requests.exceptions.ConnectionError as error:
    print("RESULT: CONNECTION ERROR")
    print(type(error).__name__)

except requests.exceptions.RequestException as error:
    print("RESULT: OTHER REQUEST ERROR")
    print(type(error).__name__)