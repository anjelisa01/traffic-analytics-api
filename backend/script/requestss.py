import requests

from dotenv import load_dotenv
from event_generator import generate_event

import os
load_dotenv()
api_url=os.getenv("API_URL")
# print(api_url)

# batch_url=f'{api_url}/api/events/bulk/3'



BASE_URL = f'{api_url}/api/events'
WEBSITE_ID = 3
TIMEOUT=18

events=[generate_event() for _ in range(1000)]

try:
    response = requests.post(
                    f"{BASE_URL}/bulk/{WEBSITE_ID}",
                    json=events,
                    timeout=TIMEOUT,
                )
    print("Status:", response.status_code)
    # print("Response:", response.text)
except Exception as e:
    print(e)
