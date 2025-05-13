import json
from PIL import Image
from pyproj import Transformer
import api

base_url = 'https://geo.mauniver.ru/api/'
res_url = f'{base_url}resource/'
resId = 922

def get_black_pixel_coordinates(image_path, coords_file_path):
    try:
        # 1. Загрузка координат из JSON-файла
        with open(coords_file_path, 'r') as f:
            coords_data = json.load(f)
        min_lon = coords_data['coords_obj']['minLon']
        max_lon = coords_data['coords_obj']['maxLon']
        min_lat = coords_data['coords_obj']['minLat']
        max_lat = coords_data['coords_obj']['maxLat']

        # 2. Открытие изображения
        img = Image.open(image_path)
        width, height = img.size

        # 3. Итерация по пикселям и поиск черных пикселей
        black_pixels = []
        for x in range(width):
            for y in range(height):
                pixel = img.getpixel((x, y))
                if isinstance(pixel, tuple):
                    if len(pixel) == 3 and pixel == (45,45,45):  # RGB
                        black_pixels.append((x, y))
                    elif len(pixel) == 4 and pixel[:3] == (45,45,45):  # RGBA
                        black_pixels.append((x, y))

        # 4. Преобразование координат пикселей в географические координаты (EPSG:4326)
        geo_coordinates_4326 = []
        for x, y in black_pixels:
            # Вычисление пропорций для долготы и широты
            lon_ratio = x / width
            lat_ratio = y / height

            # Линейное преобразование координат пикселей в географические
            lon = min_lon + (max_lon - min_lon) * lon_ratio
            lat = max_lat - (max_lat - min_lat) * lat_ratio  # Инвертируем, т.к. y=0 сверху

            geo_coordinates_4326.append((lon, lat))

        # 5. Преобразование координат из EPSG:4326 в EPSG:3857
        transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
        geo_coordinates_3857 = []
        for lon, lat in geo_coordinates_4326:
            x, y = transformer.transform(lon, lat)
            geo_coordinates_3857.append((x, y))

        return geo_coordinates_3857

    except FileNotFoundError:
        print(f"Ошибка: Файл не найден.")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка: Некорректный JSON в файле.")
        return []
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []


image_file = "image2.png"
coords_file = "coords2.txt"


black_pixel_coords = get_black_pixel_coordinates(image_file, coords_file)
if black_pixel_coords:
    print("Координаты черных пикселей в EPSG:3857 (x, y):")
    for x, y in black_pixel_coords:
        print(f"{x} {y}")
        feature_data = {
            "type": "Feature",
            "fields": {
                "ClassName": "key",
                "Year": 2025,
                "day": 7,
            },
            "geom": f"POINT ({x} {y})"
        }
        response = api.addFeature(resId, feature_data)
        if response.status_code == 200 or response.status_code == 201:
            print("Объект успешно добавлен!")
            print("Содержимое ответа:", response.json())
        else:
            print(f"Код состояния: {response.status_code}")
            print(response.text)
else:
    print("Не удалось получить координаты черных пикселей.")























# # Создаём группу ресурсов
# response = api.createResourceGroup(res_url,parentID=207,display_name="Asdf",description='zxcxvc')
# print(response)



# # Создаём векторный слой
# response = api.createVectorLayer(res_url,parentID=531,display_name='DEMO_POINT',description='DEMO',geometry_type="POINT", srs=3857,
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









