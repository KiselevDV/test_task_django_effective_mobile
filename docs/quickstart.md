# Быстрый старт через Docker


## 1. Клонируйте репозиторий

```bash
git clone https://github.com/KiselevDV/test_task_django_effective_mobile.git
cd test-task-django-effective-mobile
```


## 2. Запуск проекта

```bash
cd docker
docker-compose up -d
```

Приложение будет доступно на: http://localhost:18000

Админка: http://localhost:18000/admin/


## 3. Запуск тестов

```bash
docker exec -it backend_effective_mobile pytest
```

[Назад](../README.md)