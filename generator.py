import requests

from dotenv import load_dotenv
import os
load_dotenv()
api_url=os.getenv("API_URL")
print(api_url)

url=f'{api_url}/api/events/3'

batch_url=f'{api_url}/api/events/bulk/3'
def batch_ingestion():  #one transaction, multiple saved events
    events=[
                {
                    "event_type": "page_view",
                    "page": "/products"
                },
                {
                    "event_type": "button_click",
                    "page": "/products"
                },
                {
                    "event_type": "page_view",
                    "page": "/checkout"
                }
                ]
    response=requests.post(batch_url,json=events,timeout=18)
    print("---BATCH event ingestion---")
    print("Status:", response.status_code)
    # print("Response:", response.text)
    print("-------------------------")
    


def one_event_ingestion():
    event={
        "event_type": "page_view",
        "page":"/products",
    }
    print(url)
    response=requests.post(url,json=event,timeout=18)
    print("---ONE event ingestion---")
    print("Status:", response.status_code)
    # print("Response:", response.text)
    print("-------------------------")

def multiple_event_ingestion(): #one by one transactions
    events = [
                {
                    "website_id": 3,
                    "event_type": "page_view",
                    "page": "/products"
                },
                {
                    "website_id": 3,
                    "event_type": "button_click",
                    "page": "/products"
                },
                {
                    "website_id": 3,
                    "event_type": "page_view",
                    "page": "/checkout"
                },
                {
                    "website_id": 3,
                    "event_type": "form_submit",
                    "page": "/contact"
                }
            ]
    print("---MULITPLE event ingestion---")
    for event in events:
        response=requests.post(url,json=event,timeout=18)
        print("Status:", response.status_code)
        # print("Response:", response.text)
    print("-------------------------")
   

one_event_ingestion()
multiple_event_ingestion()
batch_ingestion()






'''

# event={
#     "event_type": "page_view",
#     "page":"/products",
#     # "timestamp":'2026-10-29 11:30:00'
# }


events = [
    {
        "website_id": 3,
        "event_type": "page_view",
        "page": "/products"
    },
    {
        "website_id": 3,
        "event_type": "button_click",
        "page": "/products"
    },
    {
        "website_id": 3,
        "event_type": "page_view",
        "page": "/checkout"
    },
    {
        "website_id": 3,
        "event_type": "form_submit",
        "page": "/contact"
    }
]


# print(event)

#endpoint url:
# url=api_url+"/api/events/3"
url='https://crowded-goblin-x5wp79r5wj9xhpj4g-8000.app.github.dev/api/events/3'

for event in events:
    response=requests.post(url,json=event,timeout=18)
    print("Status:", response.status_code)
    print("Response:", response.text)


# print(url)
# print("Status:", response.status_code)
# print("Response:", response.text)






buat request generator

url parameter: {website_id=3}

request body POST
{
    "event_type": "page_view"
    "page":"/products"
    "timestamp":'2026-10-29 11:30:00'
}

import request





'''