## Финальный проект спринта DRF курса Яндекс.Практикум
Это учебный проект демонтрирующий навыки работы с Django REST framework и создания API (программных интерфейсов)
Подробное ТЗ и описание реализованных API запросов можно получить по адресу http://127.0.0.1:8000/redoc/ после запуска проекта

## Установка
* склонируйте репозиторий https://github.com/DenisChesnokov/api_final_yatube
* в папке проекта создайте и активируйте виртуальное окружение: 
    - cd api_final_yatube
    - python3 -m venv venv
    - source venv/bin/activate (Linux, MacOS), venv/Scripts/acrivate (Win)
* установите необходимые пакеты:
    - pip install -r requirements.txt
* проведите миграции:
    - cd yatube_api
    - python manage.py makemigrations
    - python manage.py migrate
* запустите сервер разработчика
    - python manage.py runserver

Теперь можно выполнять запросы к эндпоинтам

## Примеры запросов
* ТЗ можно открыть в браузере по адресу http://127.0.0.1:8000/redoc/ 
* Создание нового поста
    - POST http://127.0.0.1:8000/api/v1/posts/ 
    {
        "text": "string",
        "image": "string",
        "group": 0
    }
* Получить список сообществ
    - GET http://127.0.0.1:8000/api/v1/groups/ 
