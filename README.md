# Проект «YaMDb» в контейнере Docker

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)
[![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)](https://www.django-rest-framework.org/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

### Описание
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 

Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

Документация доступна по адресу: ```http://127.0.0.1:8000/redoc```

## Технологии
 - Python 3.10.6
 - Django 3.2
 - REST Framework 3.12.4
 - PyJWT 2.1.0
 - Django filter 22.1
 - Gunicorn 20.0.4
 - PostgreSQL 13
 - Docker 23.0.2
 - подробнее см. прилагаемый файл зависимостей requrements.txt

### Шаблон наполнения env-файла
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД

### Описание команд для запуска приложения в контейнерах
Все нижеописанные комманды применялись на ОС Linux Ubuntu
#### Клонируем репозиторий 

```
git clone git@github.com:Alimovriq/infra_sp2.git
```
#### Переходим в папку с проектом
```
cd infra_sp2
```

#### Создаем виртуальное окружение и его активируем
```
python3 -m venv/venv
```
```
source venv/bin/activate
```

#### Устанавливаем зависимости 
```
pip install -r api_yamdb/requirements.txt
```

#### Переходим в папку infra 
```
cd infra
```

#### Поднимаем контейнеры
```
sudo docker-compose up -d --build
```
#### Делаем миграции
```
sudo docker-compose exec web python manage.py migrate auth
```
```
sudo docker-compose exec web python manage.py migrate --run-syncdb
```
#### Создаем суперюзера
```
sudo docker-compose exec web python manage.py createsuperuser
```

#### Создаем бэкап БД
```
sudo docker-compose exec web python manage.py dumpdata > fixtures.json
```
## Примеры API-запросов
Подробные примеры запросов и коды ответов приведены в прилагаемой документации в формате ReDoc 

### Автор
Алимов Ринат
https://github.com/Alimovriq