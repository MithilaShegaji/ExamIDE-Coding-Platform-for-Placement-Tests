import requests
import time
from flask import current_app

def submit_to_judge0(code, language_id, stdin, expected_output=None):
    """
    Submits code to Judge0 for execution and waits for the result.
    Can be used for both custom runs and grading against test cases.
    """
    api_host = current_app.config['JUDGE0_API_HOST']
    api_key = current_app.config['JUDGE0_API_KEY']

    headers = {
        "x-rapidapi-host": api_host,
        "x-rapidapi-key": api_key,
        "content-type": "application/json"
    }

    payload = {
        "language_id": language_id,
        "source_code": code,
        "stdin": stdin,
        "expected_output": expected_output
    }

    try:
        # Post submission and wait for the result
        resp = requests.post(
            f"https://{api_host}/submissions?base64_encoded=false&wait=true",
            headers=headers,
            json=payload,
            timeout=10 # 10-second timeout
        )
        resp.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return resp.json()

    except requests.exceptions.RequestException as e:
        # Handle connection errors, timeouts, etc.
        return {"error": True, "message": str(e)}