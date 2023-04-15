```
git clone https://github.com/salosyatov/PyRetri.git
cd Pyretri
python setup.py install
```


Чтобы подготовить файлы для поиска, нужно:
- добавить файлы в `data/own/gallery`
- выполнить команды:
```
python main/make_data_json.py -d data/own/gallery/ -sp data_jsons/own_gallery.json -t general
python main/extract_feature.py -dj data_jsons/own_gallery.json -sp data/features/own/gallery/ -cfg configs/own.yaml
```

Чтобы собрать образ:
```
docker build -t pyretri-main .
```
Чтобы повесить тэг:
```
docker image tag pyretri-main salos/pyretri-main
```
Чтоб отправить в репозиторий и вытащить из него
```
docker push salos/pyretri-main
docker pull salos/pyretri-main
```

Чтоб запустить бот:
```
docker run -d --memory="1g" pyretri-main python bot.py
```
Чтоб остановить контейнер 
```
docker container stop #container_name
```