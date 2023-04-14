Чтобы подготовить файлы для поиска, нужно выполнить команды:
```
python main/make_data_json.py -d data/own/gallery/ -sp data_jsons/own_gallery.json -t general
python main/extract_feature.py -dj data_jsons/own_gallery.json -sp data/features/own/gallery/ -cfg configs/own.yaml
```
Чтобы собрать образ:
```
docker build -t pyretri-main .
```
Чтоб запустить бот:
```
docker run -d --memory="1g" pyretri-main python bot.py
```
