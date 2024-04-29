from io import BytesIO
from PIL import Image
import requests

search_api_server = "https://search-maps.yandex.ru/v1/?text=37.532333, 55.700323&ll=37.532333,55.700323&spn=0.552069,0.400552&lang=ru_RU&apikey=dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
# api_key = "..."

# address_ll = "37.588392,55.734036"
#
# search_params = {
#     "apikey": api_key,
#     "text": "аптека",
#     "lang": "ru_RU",
#     "ll": address_ll,
#     "type": "biz"
# }

response = requests.get(search_api_server)
if not response:
    #...
    pass
# Преобразуем ответ в json-объект
json_response = response.json()

# Получаем первую найденную организацию.
organization = json_response["features"][0]
# Название организации.
org_name = organization["properties"]["CompanyMetaData"]["name"]
# Адрес организации.
org_address = organization["properties"]["CompanyMetaData"]["address"]

# Получаем координаты ответа.
point = organization["geometry"]["coordinates"]
org_point = "{0},{1}".format(point[0], point[1])
delta = "0.005"

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    # позиционируем карту центром на наш исходный адрес
    "ll": org_point,
    "spn": ",".join([delta, delta]),
    "l": "map",
    # добавим точку, чтобы указать найденную аптеку
    "pt": "{0},pm2dgl".format(org_point)
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()