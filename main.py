import api

base_url = 'https://geo.mauniver.ru/api/'
res_url = f'{base_url}resource/'
"""
# Создаём группу ресурсов
response = api.createResourceGroup(res_url,parentID=207,display_name="MAU_Oil",description='xd')
print(response)

# Создаём векторный слой
response = api.createVectorLayer(res_url,parentID=253,display_name='ppp',description='ppp',geometry_type="POINT",
                              fields=[
                                  {
                                      "keyname": "date",
                                      "display_name": "date",
                                      "datatype": "DATE"
                                  },
                                  {
                                      "keyname": "205.03.12",
                                      "display_name": "12:12:27",
                                      "datatype": "TIME"
                                  },
                              ]
                              )
print(response)
"""

point_geometry = {
    "type": "Point",
    "coordinates": [37.6173, 55.7558]
}

# Определяем атрибуты точки
point_attributes = {
    "name": "Moscow",
    "description": "Capital of Russia"
}
# Создаём точку на векторном слое
response = api.addPointToVectorLayer(res_url,layer_id=253,geometry=point_geometry,attributes=point_attributes,auth=AUTH)
print(response)
