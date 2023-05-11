<h1 align="center">Сервис друзей на DJANGO c REST API и OpenAPI спецификацией</h1>

## Содержание
[Локальный запуск сервера](#locale-launch)
[Взаимодействие с сервером](#working-with-the-service)
[База данных](#database)
[Тестирование](#testing)
## Locale launch
Для того чтобы локально запустить сервис нужно иметь установленный Docker, Docker-compose, venv.\
Запустите виртуальное окружение в рабочем каталоге и пропишите в командной строке(в рабочем каталоге) 
следующие команды:\
<code>docker-compose build docker-compose.yaml</code> для постройки базы данных.
<code>docker-compose up &</code> для запуска контейнера.\
<code>python manage.py migrate</code> для применения миграций.\
<code>python manage.py runserver</code> для запуска сервера


## Working with the service
Для того чтобы взаимодействовать с сервером нужно перейти ссылке [http://127.0.0.1:8000](http://127.0.0.1:8000).\
Всего доступны следующие пути:

### `POST /user-register` – Регистрация пользователя
Тело запроса: POST
```json
{
  "username": "string",
  "password": "string"
}
```
### `POST, DELETE /friend` - Отправка запроса в друзья/удаление друга
Тело запроса: POST
```json
{
  "from_id": 0,
  "to_id": 0
}
```
Тело запроса: DELETE
```json
{
  "user_id": 0,
  "deleting_id": 0
}
```

### `GET /friend/status` - Проверка на статус дружбы
Тело запроса: GET
```json
{
  "user_id": 0,
  "checked_user_id": 0
}
```
### `GET /friend/list` - Вывести список всех друзей пользователя
Тело запроса: GET
```json
{
  "user_id": 0
}
```
### `GET /friend/all_requests` - Получить список всех входящих и исходящих заявок
Тело запроса: GET
```json
{
  "user_id": 0
}
```
Для того чтобы сделать запрос, нужно создать супер пользователя, для этого введитев командной строке в рабочем каталоге\
`python manage.py createsuperuser`. Далее нужно перейти по нужному маршруту, авторизоваться, и ввести тело запроса в JSON-формате.
Пример: /user/register
```json
{
  "username": "Aleksei",
  "password": "Aleksei"
}
```
> [Пример POST-запроса](img_post.png)\
> [Пример DELETE-запроса](img_delete.png)


## Database
Для этого сервиса я использовал PostgreSQL в docker'е. Всего есть 3 таблицы в 
БД для хранения пользователей, запросов и друзей - `user`, `userfriend`, `friend_request` соответственно.\
Посмотреть схему можно в файле /User/models.py Я также я использовал индексы для ускорения доступа к данным, 
и атомарные операции для выполнения транзакций удаления/добавления друзьей



## Testing

Подготавливаем окружение исходя из предыдущего раздела.
Для начала нужно зарегистрировать пользователей в [http://127.0.0.1:8000/user/register](http://127.0.0.1:8000/user/register).
```json
{
  "username": "Aleksei",
  "password": "Aleksei"
}
```
```json
{
  "username": "Borya",
  "password": "Borya"
}
```
```json
{
  "username": "Valeriy",
  "password": "Valeriy"
}
```
```json
{
  "username": "Olga",
  "password": "Olga"
}
```
Для отправки запросов в друзья переходим в [http://127.0.0.1:8000/friend/](http://127.0.0.1:8000/friend) 
и отправляем запросы
```json
{
  "from_id_id": "1",
  "to_id_id": "2"
}
```
```json
{
  "from_id_id": "2",
  "to_id_id": "1"
}
```
```json
{
  "from_id_id": "1",
  "to_id_id": "3"
}
```
Так как пользователи с ID 1 и 2 отправили запросы друг другу, они теперь друзья. 
Если мы отправим один и тот же запрос дважды, мы получим ошибку 409_CONFLICT,
так как мы отправили один и тот же запрос дважды.\
\
Попробуем получить список друзей пользователя с ID 1. Для этого перейдем и сделаем GET-запрос:
[http://127.0.0.1:8000/friend/list/?user_id=1](http://127.0.0.1:8000/friend/list/?user_id=1)\
\
Теперь попробуем проверить статус отношений пользователя c ID 1 с пользователем c ID 2, для этого сделаем GET-запрос:\
[http://127.0.0.1:8000/friend/status/?user_id=1&checked_user_id=2](http://127.0.0.1:8000/friend/status/?user_id=1&checked_user_id=2)\
\
Теперь попробуем получить список всех исходящих/входящих запросов в друзья пользователя с ID 3. 
Сделаем GET-запрос в 
[http://127.0.0.1:8000/friend/all_requests/?user_id=1](http://127.0.0.1:8000/friend/all_requests/?user_id=1)\
\
Теперь удалим пользователя2 из друзей пользователя1 в [http://127.0.0.1:8000/friend/?user_id=1&deleting_id=2](http://127.0.0.1:8000/friend/?user_id=1&deleting_id=2) 
Нажав кнопку DELETE
Проверим, сделав GET-запрос на список друзей пользователя с ID 1 
[http://127.0.0.1:8000/friend/list/?user_id=1](http://127.0.0.1:8000/friend/list/?user_id=1).
