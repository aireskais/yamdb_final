# Описание:
API сервиса YaMDb, которое собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

# Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

```
git@github.com:aireskais/yamdb_final.git
```

В файле default.conf прописать IP своего сервера:

```
server {
    listen 80;
    server_name <ваш IP>;
    server_tokens off;
    location /static/ {
        root /var/html/;
    }
    location /media/ {
        root /var/html/;
    }
    location / {
        proxy_pass http://web:9000;
    }
}
```

Пушим к себе в репозиторий, и прописываем секреты:

```
DOCKER_USERNAME=<логин для докера>
DOCKER_PASSWORD=<пароль>
HOST=<IP сервера>
USER=<пользователь на сервере>
SSH_KEY=<приватный ключ от компьтера, у которого есть доступ на сервер>
PASSPHRASE=<защитный пароль для ssh ключа, если есть>
TELEGRAM_TO=<Id бота в телегра, для отправки уведомления об успешном деплое>
TELEGRAM_TOKEN=<токен для бота>
DB_ENGINE=<django.db.backends.postgresql или любой другой>
DB_NAME=<postgres или любой другой>
POSTGRES_USER=<ваш пользователь>
POSTGRES_PASSWORD=<пароль для вашего пользователя>
DB_HOST=db
DB_PORT=5432
```

Остается инициировать workflow запушив еще раз какие-либо изменения.
После удачного деплоя, на сервере выполнить миграции, создать суперпользователя и собрать статику:

```
sudo docker-compose exec web python manage.py migrate
sudo docker-compose exec web python manage.py createsuperuser
sudo docker-compose exec web python manage.py collectstatic --no-input
```

Заполнить БД тестовыми данными:

```
sudo docker-compose exec web python manage.py import_csv
```

Сервис будет доступен по адресу:

```
http://<ваш IP сервера>:9000/redoc/
```

# Попробовать можно тут:
http://51.250.17.0:9000/redoc/

# Автор проекта:
[Андрис](https://github.com/aireskais)

![example workflow](https://github.com/aireskais/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)