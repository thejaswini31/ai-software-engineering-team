import requests

url = "https://api-inference.huggingface.co/models/google/flan-t5-large"

response = requests.get(url)

print(response.status_code)
print(response.text)