```
git clone https://github.com/salosyatov/PyRetri.git
cd Pyretri
git pull
python setup.py install
```


Чтобы подготовить файлы для поиска, нужно:
- добавить файлы в `data/landmarks/gallery`
- выполнить команды:
```
pip install matplotlib
python main/make_data_json.py -d data/landmarks/gallery/ -sp data_jsons/landmarks_gallery.json -t general
python main/extract_feature.py -dj data_jsons/landmarks_gallery.json -sp data/features/landmarks/gallery/ -cfg configs/landmarks.yaml
```

Чтобы собрать образ:
```
docker build -t landmarks .
```
Чтобы повесить тэг:
```
docker image tag landmarks salos/landmarks
```
Чтоб отправить в репозиторий и вытащить из него
```
docker push salos/landmarks
docker pull salos/landmarks
```

Чтоб запустить бот:
```
docker run -d --memory="1g" landmarks python bot.py
```
Чтоб увидеть текущие контейнеры
```
docker container ls
```

Чтоб остановить и удалить контейнер 
```
docker stop <Container_ID>
docker rm <Container_ID>

```