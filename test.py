import requests

url = "https://fool-vaporizer-alibi.ngrok-free.dev"

with open("test.mp3", "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)

print("STATUS:", response.status_code)
print("RESULT:", response.text)