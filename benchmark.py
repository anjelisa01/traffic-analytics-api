
import time
import requests
import statistics

from dotenv import load_dotenv
import os
load_dotenv()
api_url=os.getenv("API_URL")


BASE_URL = f'{api_url}/api/events'
WEBSITE_ID = 3
TOTAL_EVENTS = 1000
BATCH_SIZE = 100
TIMEOUT = 30

def make_event(i):
    return {
        "event_type": (
            "page_view" if i % 2 == 0 else "button_click"
        ),
        "page": f"/page-{i % 20}"
    }

def benchmark_individual(events):
    success = 0
    start = time.perf_counter()

    for event in events:
        try:
            response = requests.post(
                f"{BASE_URL}/{WEBSITE_ID}",
                json=event,
                timeout=TIMEOUT,
            )
            if response.ok:
                success += 1
            else:
                print(
                    f"Individual failed: "
                    f"status={response.status_code}, "
                    f"body={response.text}"
                )
        except requests.RequestException as exc:
            pass
            # print("Individual request error:", exc)

    elapsed = time.perf_counter() - start
    return elapsed, success

def benchmark_batches(events):
    success = 0
    start = time.perf_counter()

    for i in range(0, len(events), BATCH_SIZE):
        batch = events[i:i + BATCH_SIZE]

        try:
            response = requests.post(
                f"{BASE_URL}/bulk/{WEBSITE_ID}",
                json=batch,
                timeout=TIMEOUT,
            )

            if response.ok:
                success += len(batch)
            else:
                print(
                    f"Batch failed: "
                    f"status={response.status_code}, "
                    f"body={response.text}"
                )
        except requests.RequestException as exc:
            pass
            # print("Batch request error:", exc)

    elapsed = time.perf_counter() - start
    return elapsed, success

def report(name, elapsed, success):
    print(f"\n{name}")
    print(f"Duration:       {elapsed:.2f} seconds")
    print(f"Successful:     {success}/{TOTAL_EVENTS}")
    print(f"Events/second:  {success / elapsed:.2f}")
    print(f"Success rate:   {success / TOTAL_EVENTS * 100:.1f}%")

if __name__ == "__main__":
    events = [make_event(i) for i in range(TOTAL_EVENTS)]

    print(f"Testing {TOTAL_EVENTS} events...")
    print("Ensure your API and database are running.")

    individual_time, individual_success = benchmark_individual(events)
    batch_time, batch_success = benchmark_batches(events)

    report("Individual requests", individual_time, individual_success)
    report("Batch requests", batch_time, batch_success)

    if batch_time > 0:
        print(
            "\nBatch speedup:",
            f"{individual_time / batch_time:.2f}x"
        )
