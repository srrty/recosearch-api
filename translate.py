import requests

def translate_to_korean(text: str) -> str:
    url = "https://libretranslate.de/translate"
    payload = {"q": text, "source": "en", "target": "ko", "format": "text"}
    resp = requests.post(url, data=payload, timeout=10.0)
    resp.raise_for_status()
    return resp.json().get("translatedText", text)
