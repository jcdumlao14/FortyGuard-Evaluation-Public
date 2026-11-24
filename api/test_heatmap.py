import json
import os
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

# --------------------------------------------------
# FortyGuard Heatmap API Test
# --------------------------------------------------

BASE_URL = "https://api.fortyguard.com/v1"
HEATMAP_URL = f"{BASE_URL}/heatmap"

PROJECT_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

load_dotenv(PROJECT_DIR / ".env")

API_KEY = os.getenv("FORTYGUARD_API_KEY")

# Documented example request from FortyGuard
PAYLOAD = {
    "polygon_aoi": {
        "type": "Polygon",
        "coordinates": [[
            [-74.0170, 40.7051],
            [-74.0031, 40.7051],
            [-74.0031, 40.7180],
            [-74.0170, 40.7180],
            [-74.0170, 40.7051]
        ]]
    },
    "date_time": {
        "start_date": "2024-07-15",
        "start_time": "14:00",
        "filter_type": 1
    },
    "granularity": 100
}

HEADERS = {
    "api-key": API_KEY or "",
    "Content-Type": "application/json"
}

POLL_INTERVAL = 5
MAX_ATTEMPTS = 120


def save_json(filename, data):
    """Save JSON results locally."""
    path = RESULTS_DIR / filename

    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    print(f"Saved: {path}")
    return path


def extract_activity_id(data):
    """Support common response structures."""
    if not isinstance(data, dict):
        return None

    activity_id = data.get("activity_id")

    if activity_id:
        return activity_id

    nested = data.get("data")

    if isinstance(nested, dict):
        return nested.get("activity_id")

    return None


def extract_status(data):
    """Extract task status from common response structures."""
    if not isinstance(data, dict):
        return "unknown"

    for key in ("status", "activity_status", "state"):
        value = data.get(key)
        if isinstance(value, str):
            return value.strip().lower()

    nested = data.get("data")

    if isinstance(nested, dict):
        for key in ("status", "activity_status", "state"):
            value = nested.get(key)
            if isinstance(value, str):
                return value.strip().lower()

    return "unknown"


def main():
    print("=" * 60)
    print("FORTYGUARD - HEATMAP API TEST")
    print("=" * 60)

    if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
        print("ERROR: API key not found in your .env file.")
        return

    print("\nAPI key: Loaded securely")
    print("Endpoint:", HEATMAP_URL)
    print("Method: POST")
    print("Granularity:", PAYLOAD["granularity"], "metres")
    print("Date:", PAYLOAD["date_time"]["start_date"])
    print("Time:", PAYLOAD["date_time"]["start_time"])
    print("Filter type: Single Hour (1)")

    print("\nRequest payload:")
    print(json.dumps(PAYLOAD, indent=2))

    print("\nIMPORTANT:")
    print("This request can consume API credits upon successful completion.")
    print("Documented cost: 3,500 credits (Basic/Startup)")
    print("Documented cost: 4,220 credits (Premium)")
    print("Check your plan and available credits before proceeding.")

    confirmation = input(
        "\nType SUBMIT to send this actual API request: "
    ).strip()

    if confirmation != "SUBMIT":
        print("\nRequest cancelled. No API request was sent.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print("\nSubmitting heatmap request...")

    try:
        response = requests.post(
            HEATMAP_URL,
            headers=HEADERS,
            json=PAYLOAD,
            timeout=60
        )

        print("HTTP status:", response.status_code)

        try:
            submission_data = response.json()
        except ValueError:
            submission_data = {"raw_response": response.text}

        save_json(
            f"heatmap_submission_{timestamp}.json",
            {
                "http_status": response.status_code,
                "request_payload": PAYLOAD,
                "response": submission_data
            }
        )

        if response.status_code != 200 and not response.ok:
            print("Submission failed.")
            print(json.dumps(submission_data, indent=2))
            return

        activity_id = extract_activity_id(submission_data)

        if not activity_id:
            print("Could not find activity_id in the response.")
            print("Please inspect the saved submission file.")
            return

        print("\nActivity ID:", activity_id)
        print("Heatmap task submitted successfully.")

    except requests.RequestException as error:
        print("Network or request error:", str(error))
        return

    # --------------------------------------------------
    # Poll task status
    # --------------------------------------------------

    status_url = f"{BASE_URL}/status/{activity_id}"

    print("\nMonitoring task status...")
    print("Status endpoint:", status_url)

    final_data = None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(
            f"\nAttempt {attempt}/{MAX_ATTEMPTS}"
        )

        try:
            status_response = requests.get(
                status_url,
                headers=HEADERS,
                timeout=30
            )

            print("HTTP status:", status_response.status_code)

            # Documentation notes that 404 can occur temporarily
            # after task submission.
            if status_response.status_code == 404:
                print("Task not available yet. Retrying...")
                time.sleep(POLL_INTERVAL)
                continue

            if status_response.status_code == 429:
                print("Rate limited. Waiting before retry...")
                time.sleep(15)
                continue

            status_response.raise_for_status()

            status_data = status_response.json()
            current_status = extract_status(status_data)

            print("Task status:", current_status)

            if current_status in ("completed", "succeeded", "success"):
                final_data = status_data
                print("\nHeatmap generation completed!")
                break

            if current_status in ("failed", "error"):
                final_data = status_data
                print("\nHeatmap generation failed.")
                break

            if current_status == "unknown":
                print("Status field not recognized.")
                print("Response:", json.dumps(status_data, indent=2))

            time.sleep(POLL_INTERVAL)

        except requests.RequestException as error:
            print("Status request error:", str(error))
            time.sleep(POLL_INTERVAL)

        except ValueError:
            print("Status endpoint returned invalid JSON.")
            time.sleep(POLL_INTERVAL)

    # --------------------------------------------------
    # Save final result
    # --------------------------------------------------

    if final_data is not None:
        save_json(
            f"heatmap_result_{timestamp}.json",
            {
                "activity_id": activity_id,
                "final_response": final_data
            }
        )

        print("\nFinal response saved.")

    else:
        print("\nPolling limit reached.")
        print("The task may still be processing.")
        print("Save the activity ID for a later status check:")
        print(activity_id)

    print("\nAPI test finished.")
    print("Check the results folder for saved JSON files.")


if __name__ == "__main__":
    main()
