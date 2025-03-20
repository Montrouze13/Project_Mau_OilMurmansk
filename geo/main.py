import api

base_url = 'https://geo.mauniver.ru/api/'
res_url = f'{base_url}resource/'

# # Создаём группу ресурсов
# response = api.createResourceGroup(res_url,parentID=207,display_name="Asdf",description='zxcxvc')
# print(response)



# # Создаём векторный слой
# response = api.createVectorLayer(res_url,parentID=251,display_name='ppppp',description='ppp',geometry_type="POINT", srs=3857,
#                               fields=[
#                                   {
#                                       "keyname": "date",
#                                       "display_name": "date",
#                                       "datatype": "DATE",
#                                   },
#                                   {
#                                       "keyname": "2025.03.12",
#                                       "display_name": "12:02:27",
#                                       "datatype": "TIME",
#                                   },
#                               ]
#                               )
# print(response)

feature_data = {
    "type": "Feature",
    "fields": {
      "ClassName":"key",
        "Year":2025,
        "day": 7,
    },
    "geom":"Polygon ((79.87749999947846 6.997500000409782, 79.88249999947845 6.997500000409782, 79.88249999947845 7.002500000409782, 79.87749999947846 7.002500000409782, 79.87749999947846 6.997500000409782))"
}

resId = 253
response = api.addFeature(resId, feature_data)

if response.status_code == 200 or response.status_code == 201:
    print("Объект успешно добавлен!")
    print("Содержимое ответа:", response.json())
else:
    print(f"Код состояния: {response.status_code}")
    print(response.text)

