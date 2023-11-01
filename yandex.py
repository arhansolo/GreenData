import requests
import xmltodict

from settings import YANDEX_ADDRESS, YANDEX_API_KEY

base_url = "https://geocode-maps.yandex.ru/1.x/"
response = requests.get(base_url, params={
    "geocode": YANDEX_ADDRESS,
    "apikey": YANDEX_API_KEY,
    "format": "json",  # либо меняем на параметр "xml"
})
response.raise_for_status()
print(response.json())
# для xml
# dict_data = xmltodict.parse(response.content)
# print(dict_data)
