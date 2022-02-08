# api_yamdb
REST API для сервиса YaMDb, который собирает отзывы пользователей на произведения, с возможностью комментирования отзывов.

** Установка **
Скопировать код из репозитория:
`git clone https://github.com/aleksandrtikhonov/api_yamdb.git`
Выполнить миграции базы данных:
`python /api_yamdb/manage.py makemigrations` 
`python /api_yamdb/manage.py migrate`
Опционально можно загрузить готовые данные в БД и CSV файла
Команда для загрузки вызывается с аргументами "путь к файлу" и "модель".
Например для загрузки пользователей:
`python /api_yamdb/manage.py importcsv static/data/users.csv User`

** Запуск приложения **
`python /api_yamdb/manage.py runserver`

Документация по доступным методам будет раположена по адресу:
`127.0.0.1:8000/redoc`