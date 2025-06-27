import json
from PIL import Image
from pyproj import Transformer
import api
import datetime
import os

base_url = 'https://geo.mauniver.ru/api/'
res_url = f'{base_url}resource/'

# Функция для создания группы ресурсов
def create_resource_group_interactive(res_url):
    parentID = input("Введите parentID для группы ресурсов: ")
    display_name = input("Введите display_name для группы ресурсов: ")
    description = input("Введите description для группы ресурсов: ")
    try:
        response = api.createResourceGroup(res_url, parentID=int(parentID), display_name=display_name, description=description)
        print(response.json())
        return response.json().get('resource', {}).get('id')
    except Exception as e:
        print(f"Ошибка при создании группы ресурсов: {e}")
        return None

# Функция для создания векторного слоя
def create_vector_layer_interactive(res_url):
    parentID = input("Введите parentID для векторного слоя: ")
    display_name = input("Введите display_name для векторного слоя: ")
    description = input("Введите description для векторного слоя: ")
    try:
        response = api.createVectorLayer(res_url, parentID=int(parentID), display_name=display_name, description=description, geometry_type="POINT", srs=3857,
                                      fields=[
                                          {
                                              "keyname": "date",
                                              "display_name": "Дата",
                                              "datatype": "STRING",
                                          },
                                          {
                                              "keyname": "obs_time",
                                              "display_name": "Время",
                                              "datatype": "STRING",
                                          },
                                          {
                                              "keyname": "nearest_city",
                                              "display_name": "Ближайший населенный пункт",
                                              "datatype": "STRING",
                                          },
                                      ])
        print(response.json())
        return response.json().get('id')
    except Exception as e:
        print(f"Ошибка при создании векторного слоя: {e}")
        return None

# Функция для получения координат черных пикселей
def get_black_pixel_coordinates(image_path, coords_file_path):
    try:
        with open(coords_file_path, 'r') as f:
            coords_data = json.load(f)
        min_lon = coords_data['coords_obj']['minLon']
        max_lon = coords_data['coords_obj']['maxLon']
        min_lat = coords_data['coords_obj']['minLat']
        max_lat = coords_data['coords_obj']['maxLat']

        img = Image.open(image_path)
        width, height = img.size

        black_pixels = []
        for x in range(width):
            for y in range(height):
                pixel = img.getpixel((x, y))
                if isinstance(pixel, tuple):
                    if len(pixel) == 3 and pixel == (45, 45, 45):
                        black_pixels.append((x, y))
                    elif len(pixel) == 4 and pixel[:3] == (45, 45, 45):
                        black_pixels.append((x, y))

        geo_coordinates_4326 = []
        for x, y in black_pixels:
            lon_ratio = x / width
            lat_ratio = y / height
            lon = min_lon + (max_lon - min_lon) * lon_ratio
            lat = max_lat - (max_lat - min_lat) * lat_ratio
            geo_coordinates_4326.append((lon, lat))

        transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
        geo_coordinates_3857 = []
        for lon, lat in geo_coordinates_4326:
            x, y = transformer.transform(lon, lat)
            geo_coordinates_3857.append((x, y))

        return geo_coordinates_3857

    except FileNotFoundError:
        print(f"Ошибка: Файл не найден")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка: Некорректный JSON в файле")
        return []
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []



# 1. Создание группы ресурсов (опционально)
create_group = input("Создать группу ресурсов? (y/n): ").lower()
resource_group_id = None
if create_group == 'y':
    resource_group_id = create_resource_group_interactive(res_url)

# 2. Создание векторного слоя (опционально)
create_layer = input("Создать векторный слой? (y/n): ").lower()
vector_layer_id = None
if create_layer == 'y':
    vector_layer_id = create_vector_layer_interactive(res_url)
    if vector_layer_id:
        resId = vector_layer_id
    else:
        print("Не удалось создать векторный слой, дальнейшая работа невозможна")
        exit()

if vector_layer_id is None:
    resId = input("Введите ID существующего векторного слоя: ")
    try:
        resId = int(resId)
    except ValueError:
        print("Некорректный ID слоя")
        exit()


# 3. Выбор файла снимка
files_name = input("Введите имя файла снимка (без расширения): ")
image_file = f"{files_name}.png"
coords_file = f"{files_name}.txt"

# Проверяем, существуют ли файлы
if not os.path.exists(image_file):
    print(f"Ошибка: Файл снимка '{image_file}' не найден")
    exit()
if not os.path.exists(coords_file):
    print(f"Ошибка: Файл координат '{coords_file}' не найден")
    exit()


# 4. Запуск обработки и добавление объектов
black_pixel_coords = get_black_pixel_coordinates(image_file, coords_file)

if black_pixel_coords:
    today = datetime.date.today()
    date_string = today.strftime("%Y-%m-%d")
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    nearest_city = input("Введите ближайший населенный пункт: ")

    print("Координаты черных пикселей в EPSG:3857 (x, y):")
    for x, y in black_pixel_coords:
        print(f"{x} {y}")
        feature_data = {
            "type": "Feature",
            "fields": {
                "obs_time": current_time,
                "date": date_string,
                "nearest_city": nearest_city
            },
            "geom": f"POINT ({x} {y})"
        }
        try:
            response = api.addFeature(resId, feature_data)
            if response.status_code == 200 or response.status_code == 201:
                print("Объект успешно добавлен!")
                print("Содержимое ответа:", response.json())
            else:
                print(f"Код состояния: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"Ошибка при добавлении объекта: {e}")
else:
    print("Не удалось получить координаты черных пикселей")