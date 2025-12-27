📌 Задача 3. Бэкенд-часть приложения

    Язык: Python  
    Фреймворк: FastAPI  
    OLAP-база: ClickHouse  
    Аутентификация: Keycloak 21.1  
    Фронтенд: React + TypeScript
    ETL выполняется через Airflow DAG
🚀 Быстрый старт
Требования

    Docker  
    Docker Compose  
    Git  
    npm (для сборки фронтенда)

Запуск проекта

    # 1. Установите зависимости фронтенда
    cd frontend
    npm install
    cd ..
    
    # 2. Очистите всё (если запускали раньше)
    docker-compose down -v --remove-orphans
    
    # 3. Пересоберите и запустите
    docker-compose build frontend
    docker-compose up -d
```

Доступные сервисы:

    Фронтенд: http://localhost:3000
      
    Keycloak Admin: http://localhost:8081
     (admin / admin)

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

Проверка данных в ClickHouse
    docker exec -i architecture-bionicpro-clickhouse-1 clickhouse-client --query="SELECT * FROM reports.user_reports;"

Очистка и перезапуск
    # Остановить все сервисы и удалить тома
    docker-compose down -v
    
    # Удалить локальные данные ClickHouse (если использовался том)
    if (Test-Path clickhouse-data) {
        Remove-Item -Recurse -Force clickhouse-data
    }
    
    # Запустить заново
    docker-compose up -d
