
import random
from datetime import datetime, timedelta, timezone
from uuid import uuid4

PAGES = ["/", "/products", "/pricing", "/about", "/signup"]
TYPE=['page_views','button_click','submit_form']

def generate_event() -> dict:
    now = datetime.now(timezone.utc)
    event_time = now - timedelta(
        seconds=random.randint(0, 7 * 24 * 60 * 60)
    )

    return {
        "event_type":random.choice(TYPE),
        "page": random.choice(PAGES),
        "timestamp": event_time.isoformat(),
    }


# events = [generate_event() for _ in range(3)]

# print(f"Generated {len(events)} events")


# for event in events:
#     print(event)

# print()
