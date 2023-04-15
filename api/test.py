import base64
import os.path

import PIL
import requests

API_ENDPOINT = "http://localhost:5000/api/top_k"

path = 'data/caltech101/query/panda.jpg'
print(os.path.exists(path))

image = PIL.Image.open(path).convert("RGB")
k=6

with open(path, 'rb') as f:
    im_b64 = base64.b64encode(f.read())


data = {

    'image': im_b64
}
response = requests.post(url=API_ENDPOINT, data=data, timeout=120)
top_similar = response.json()
print(top_similar)
