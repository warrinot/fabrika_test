# fabrika_test
Тестовое Задание

У текущего тестового задания есть только общее описание требований, конкретные детали реализации остаются на усмотрение разработчика.

### Задача: спроектировать и разработать API для системы опросов пользователей.

#### Функционал для администратора системы:

- авторизация в системе (регистрация не нужна)
- добавление/изменение/удаление опросов. Атрибуты опроса: название, дата старта, дата окончания, описание. После создания поле "дата старта" у опроса менять нельзя
- добавление/изменение/удаление вопросов в опросе. Атрибуты вопросов: текст вопроса, тип вопроса (ответ текстом, ответ с выбором одного варианта, ответ с выбором нескольких вариантов)

#### Функционал для пользователей системы:

- получение списка активных опросов
- прохождение опроса: опросы можно проходить анонимно, в качестве идентификатора пользователя в API передаётся числовой ID, по которому сохраняются ответы пользователя на вопросы; один пользователь может участвовать в любом количестве опросов
- получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по ID уникальному пользователя

#### Использовать следующие технологии: Django 2.2.10, Django REST framework.

#### Результат выполнения задачи:
- исходный код приложения в github (только на github, публичный репозиторий)
- инструкция по разворачиванию приложения (в docker или локально)
- документация по API


## Деплой

### Для развертывания проекта выполнить:
 ```
 mkdir fabrika_test
 cd fabrika_test
 git init
 git pull https://github.com/warrinot/fabrika_test.git
 pip install virtualenv
 python -m venv venv
 source venv/bin/activate //на Linux или "venv\scripts\activate" на Windows
 pip install -r requirements.txt
 python manage.py migrate
 python manage.py loaddata testdata.json
 python manage.py runserver
 ```
## Документация:
#### Документация админа
##### Для всех запросов админа следует использовать login:password ```admin:123``` 
например ```curl -u admin:123 http://127.0.0.1:8000/admin_api/polls/```
##### `/admin_api/` - корневой url api для админа
##### `/admin_api/polls/` - api для управления опросами:
 - `GET` - выдает список всех опросов
 - `POST` - добавляет опрос. В теле запроса отправляется:
    ```
    {
    "name": "123",
    "description": "321"
    }
    ```
##### `/admin_api/polls/<id>` - api конкретного опроса:
- `GET` получает данные опроса
- `PUT` или `PATCH` редактируют опрос. Пример тела запроса:
    ```
    {
    "name": "321",
    "description": "123"
    }
    ```
- `DELETE` - удаляет опрос


##### `/admin_api/questions/` - api для управления вопросами
 - `GET` - выдает список всех вопросов
 - `POST` - добавляет вопрос. В теле запроса отправляется:
    ```
    {
    "poll": 1,
    "text": "Текст",
    "question_type": 2
    }
    ```
    
##### `/admin_api/questions/<id>` - api конктрентного вопроса:
- `GET` получает данные опроса
- `PUT` или `PATCH`  - редактируют опрос. Пример тела запроса:
    ```
    {
    "poll": 1,
    "text": "Новый Текст",
    "question_type": 3
    }
    ```
- `DELETE` - удаляет опрос


##### `/admin_api/choices/` - api для управления вариантом ответа
 - `GET` - выдает список всех вариантов
 - `POST` - добавляет вариант. В теле запроса отправляется:
    ```
    {
    "question": 1,
    "text": "Опция 1"
    }
    ```
    
##### `/admin_api/choices/<id>` - api конктрентного варианта ответа:
- `GET` получает данные варианта
- `PUT` или `PATCH`  - редактируют вариант. Пример тела запроса:
    ```
    {
    "question": 2,
    "text": "Опция 2"
    }
    ```
- `DELETE` - удаляет вариант

#### Документация пользователя

##### `/user_api/` - корневой url для запросов пользователей
##### `/user_api/active_polls` - метод `GET` - получение списка активных опросов пользователем
##### `/user_api/polls_finished_by_user/` - метод `GET` - получение списка опросов, в которых пользователь ответил хотя бы на 1 вопрос.
в теле запроса нужно отправить "user_id", например:
   ```
   {
   "user_id": 42
   }
   ```
##### `/user_api/user_choices/` - метод `POST` - ответ пользователя на вопрос из опроса. Если тип вопроса - "ответ текстом" в теле запроса нужно отправить:
    {
    "question": 13,
    "user_id": 321,
    "text_choice": "Текст ответа"
    }
##### Если тип вопроса - "ответ с выбором одного варианта" или "ответ с выбором нескольких вариантов", отправляется:
    {
    "question": 13,
    "choice": [
        41
    ],
    "user_id": 321
    }
    
