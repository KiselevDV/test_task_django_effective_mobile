# Команды


## 1. Миграции

```bash
docker exec -it backend_effective_mobile python manage.py makemigrations
docker exec -it backend_effective_mobile python manage.py migrate
```


## 2. Cоздать суперпользователя

```bash
docker exec -it backend_effective_mobile python manage.py createsuperuser
```


## 3. Сбор статики вручную

```bash
docker exec -it backend_effective_mobile python manage.py collectstatic --noinput
```


## 4. Доступ в контейнер

```bash
docker exec -it backend_effective_mobile sh
```

[Назад](../README.md)