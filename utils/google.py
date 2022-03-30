import requests
import json
import os

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("SPOTS_KEY")

address_search = "522 E Green St, Champaign, IL 61820".replace(" ", "%20")

URL = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="+ address_search + \
        "&inputtype=textquery&fields=name,formatted_address,geometry,type,business_status,permanently_closed&key="+ api_key

if __name__ == "__main__":
    response = requests.get(URL).json()
    print(response)
