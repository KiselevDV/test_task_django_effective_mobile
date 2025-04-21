# Команды


## 1. Миграции

```bash
docker exec -it backend_effective_mobile python manage.py migrate
```


## 2. Сбор статики вручную

```bash
docker exec -it backend_effective_mobile python manage.py collectstatic --noinput
```


## 3. Доступ в контейнер

```bash
docker exec -it backend_effective_mobile sh
```

[Назад](../README.md)