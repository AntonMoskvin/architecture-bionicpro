📌 Задача 3. Бэкенд-часть приложения

    Язык: Python  
    Фреймворк: FastAPI  
    OLAP-база: ClickHouse  
    Аутентификация: Keycloak 21.1  
    Фронтенд: React + TypeScript

🚀 Быстрый старт
Требования

    Docker  
    Docker Compose  
    Git  
    npm (для сборки фронтенда)

Запуск проекта

    1.Установите зависимости фронтенда (требуется для генерации package-lock.json):

```
cd frontend
npm install
cd ..
```

    2.Соберите и запустите все сервисы:

```
docker-compose build frontend
docker-compose up -d
```

    3.Инициализация ClickHouse
    Перед первым использованием необходимо вставить тестовые данные.

    Зайдите в Keycloak Admin: http://localhost:8080
     → admin / admin
    Перейдите в reports-realm → Users → prothetic1 → скопируйте ID пользователя
    Откройте файл clickhouse/init.sql и замените YOUR_USER_ID на скопированный ID
    Выполните инициализацию:

```
# Windows (PowerShell)
Get-Content clickhouse\init.sql | docker exec -i architecture-bionicpro-clickhouse-1 clickhouse-client --multiquery
```

Доступные сервисы:

    Фронтенд: http://localhost:3000
      
    Keycloak Admin: http://localhost:8080
     (admin / admin)  
    API Docs (Swagger): http://localhost:8001/docs
      
    ClickHouse: порт 9000

Тестовые пользователи:

    prothetic1 / prothetic123 (роль: prothetic_user)  
    prothetic2 / prothetic123  
    prothetic3 / prothetic123

Сценарий проверки

    Откройте http://localhost:3000
    Нажмите Login  
    Введите prothetic1 / prothetic123  
    Нажмите Download Report  
    Убедитесь, что отображаются данные:
    {
    "user_id": "YOUR_USER_ID",
    "report_date": "2025-12-26",
    "total_actions": 150,
    "avg_latency_ms": 82.7
    }

Проверка API напрямую

    1.Получите токен через DevTools → Console: copy(window.keycloak.token)
    2.Выполните запрос: curl.exe -H "Authorization: Bearer <ВАШ_ТОКЕН>" http://localhost:8001/reports
    3.Ожидаемый результат: JSON с отчётом.

Проверка данных в ClickHouse

    docker exec -i architecture-bionicpro-clickhouse-1 clickhouse-client --query "
    SELECT * FROM reports.user_reports;
    "

Очистка и перезапуск


    # Остановить все сервисы и удалить тома
    docker-compose down -v
    
    # Удалить локальные данные ClickHouse (если использовался том)
    if (Test-Path clickhouse-data) {
        Remove-Item -Recurse -Force clickhouse-data
    }
    
    # Запустить заново
    docker-compose up -d
