import api

base_url = 'https://geo.mauniver.ru/api/'
res_url = f'{base_url}resource/'

# # Создаём группу ресурсов
# response = api.createResourceGroup(res_url,parentID=207,display_name="Mau_Oil",description='')
# print(response)

# Создаём векторный слой
response = api.createVectorLayer(res_url,parentID=263,display_name='test123',description='',geometry_type="POINT",
                              fields=[
                                  {
                                      "keyname": "date",
                                      "display_name": "date",
                                      "datatype": "DATE"
                                  },
                                  {
                                      "keyname": "2025.03.12",
                                      "display_name": "12:12:27",
                                      "datatype": "TIME"
                                  },
                              ]
                              )
print(response)