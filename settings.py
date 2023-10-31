import os
from dotenv import load_dotenv

load_dotenv()

# 1. Dadata.ru
DADATA_ADDRESS = os.environ['DADATA_ADDRESS']
DADATA_TOKEN = os.environ['DADATA_TOKEN']
DADATA_SECRET = os.environ['DADATA_SECRET']
POSTAL_CODE_FILTER = os.environ['POSTAL_CODE_FILTER']

# 2. Yandex.Maps
YANDEX_ADDRESS = os.environ['YANDEX_ADDRESS']
YANDEX_API_KEY = os.environ['YANDEX_API_KEY']
