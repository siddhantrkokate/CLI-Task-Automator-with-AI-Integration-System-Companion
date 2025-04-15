import requests
import json

def generate(user_input, system_instructions=None):
    GEMINI_API_KEY = "AIzaSyBWXMcBCbajjasncf2fWF9KNWAVGYfD-WY"  # replace this
    MODEL_ID = "gemini-2.0-flash"
    GENERATE_CONTENT_API = "generateContent"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_ID}:{GENERATE_CONTENT_API}?key={GEMINI_API_KEY}"

    parts = []
    
    if system_instructions:
        parts.append({"text": system_instructions})
    
    parts.append({"text": user_input})

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": parts
            }
        ],
        "generationConfig": {
            "responseMimeType": "text/plain",
            "maxOutputTokens": 10000
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code != 200:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
        return None

    try:
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, json.JSONDecodeError):
        print("Failed to parse response.")
        return response.text
