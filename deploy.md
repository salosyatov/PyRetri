```
git clone https://github.com/salosyatov/PyRetri.git
cd Pyretri
git pull
python setup.py install
```


Чтобы подготовить файлы для поиска, нужно:
- добавить файлы в `data/own/gallery`

Чтобы выполнить аугментацию:
```
pip install albumentations
python main/augment.py -f data/own/gallery/

```
- выполнить команды:
```
pip install matplotlib
python main/make_data_json.py -d data/own/gallery/ -sp data_jsons/own_gallery.json -t general
python main/extract_feature.py -dj data_jsons/own_gallery.json -sp data/features/own/gallery/ -cfg configs/own.yaml
```

Чтобы собрать образ:
```
docker build -t pyretri-main:gpt .
```
Чтобы повесить тэг:
```
docker image tag pyretri-main:gpt salos/pyretri-main:gpt
```
Чтоб отправить в репозиторий и вытащить из него
```
docker push salos/pyretri-main:gpt
docker pull salos/pyretri-main:gpt
```

Чтоб запустить бот:
```
docker run -d --memory="1g" salos/pyretri-main:gpt python bot.py
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