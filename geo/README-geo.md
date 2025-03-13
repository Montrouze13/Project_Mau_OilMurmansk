# Примеры работы с геопорталом университета

# Создание ресурса "Папка"

```shell
curl --user "student1:ZfE-4wz-P3F-D2s" -H "Accept: */*" -X POST -d '{"resource": {"cls": "resource_group", "display_name": "foldername", "
parent": {"id": 207},"description" : "Folder created from curl"} }' https://geo.mauniver.ru/api/resource/
```