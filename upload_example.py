import requests

# Url auf den Server mit entsprechendem Port
url = 'http://localhost:5000/upload'
filename = 'test.jpg'  # Name des Files welches ge
with open(filename, 'rb') as file:
    files = {'image': (filename, file, "multipart/from-data")]
    response = requests.post(url, files=files)
