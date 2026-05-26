import requests

url = "https://fool-vaporizer-alibi.ngrok-free.dev/process"

with open("test.mp3", "rb") as f:
    files = {"file": ("test.mp3", f, "audio/mpeg")}
    response = requests.post(url, files=files)

print("STATUS:", response.status_code)
print("RESULT:", response.text)