import requests

API_KEY = 'AIzaSyDFTNZaSNewgkAdyM_Rl_rbYRA0kYfCUCA'
url = 'https://api.gemini.com/v1/moderation'


def moderate_content_with_gemini(content: str) -> bool:
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'input_text': content,
        'task': 'content_moderation'
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        print("Gemini API Result:", result)
        return result.get('is_offensive', False)
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return False