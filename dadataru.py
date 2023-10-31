from dadata import Dadata
import jmespath

from settings import DADATA_ADDRESS, DADATA_SECRET, DADATA_TOKEN, POSTAL_CODE_FILTER

dadata = Dadata(DADATA_TOKEN, DADATA_SECRET)

with dadata:
    dadata_source = dadata.clean(name="address", source=DADATA_ADDRESS)
    postal_code = jmespath.search("postal_code", dadata_source)

    if postal_code != POSTAL_CODE_FILTER:
        print("Запрос не прошёл по почтовому индексу!")
    else:
        print(dadata_source)
