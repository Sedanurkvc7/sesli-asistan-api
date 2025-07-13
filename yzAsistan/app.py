import requests
import json

# Test verisi
data = {
    "callerId": "+902422223344",
    "transcript": "Bu hizmet hiç yardımcı olmadı!"
}

# POST isteği gönder
response = requests.post(
    "http://localhost:5000/call-hook",
    json=data,
    headers={"Content-Type": "application/json"}
)

print("Yanıt:")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))