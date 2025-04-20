import requests
import json

def gemini(user_input, system_instructions=None):
    GEMINI_API_KEY = ""  # replace this
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

def generate_text(text):
    api_key = ""
    model_name = "Llama-3.3-70B-Instruct"
    messages = [
        {"role": "user", "content": text}
    ]
    url = "https://cloud.olakrutrim.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": model_name,
        "messages": messages,
        "frequency_penalty": 0,
        "logprobs": True,
        "top_logprobs": 2,
        "max_tokens": 5000,
        "n": 1,
        "presence_penalty": 0,
        "response_format": {"type": "text"},
        "stream": False,
        "temperature": 0,
        "top_p": 1
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as exc:
        return f"Exception: {exc}"
