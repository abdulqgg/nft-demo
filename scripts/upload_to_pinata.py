import os
from pathlib import Path
from urllib import response
import requests

Pinata_Base_Url = "https://api.pinata.cloud/"
endpoint = "pinning/pinFileToIPFS"
filepath = "./img/pug.png"
filename = filepath.split("/")[-1:][0]
headers = {
    "pinata_api_key": os.getenv("PINATA_API_KEY"), 
    "pinata_secret_api_key": os.getenv("PINATA_API_SECRET")
}

def main():
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        response = requests.post(
            Pinata_Base_Url+endpoint, 
            files={"file": (filename, image_binary)},
            headers=headers        
        )
        print(response.json())