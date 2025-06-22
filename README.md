# Telegram AI Bot

Telegram бот с AI-агентом на базе FastAPI backend для обработки пользовательских запросов с помощью OpenAI GPT.

## 🚀 Особенности

- **Telegram Bot**: Полнофункциональный бот с обработкой команд и сообщений
- **AI Agent**: Интеграция с OpenAI GPT для умных ответов
- **FastAPI Backend**: Высокопроизводительный API для обработки запросов
- **Persistent Memory**: Сохранение контекста разговора в PostgreSQL
- **Docker Support**: Полная контейнеризация приложения
- **Comprehensive Testing**: Unit и интеграционные тесты
- **Security**: Аутентификация, валидация данных, безопасное хранение токенов

## 🏗️ Архитектура

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Telegram Bot  │────│ FastAPI Backend │────│   PostgreSQL    │
│   (aiogram 3)   │    │   (AI Agent)    │    │ (Conversations) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                │
                       ┌─────────────────┐
                       │   OpenAI API    │
                       │ (GPT-3.5 Turbo) │
                       └─────────────────┘
```

## 🛠️ Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/abdusattor1999/ai-chatbot
```

### 2. Настройка окружения

```bash
# Копируем файл конфигурации
cp .env.example .env

# Редактируем .env файл
nano .env
```

Заполните следующие переменные в `.env`:

```env
# Telegram Bot
TELEGRAM_TOKEN=

# OpenAI
OPENAI_API_KEY=
OPENAI_MODEL=gpt-3.5-turbo

# Database
POSTGRES_DB=postgres
DB_PORT=
POSTGRES_USER=chatbot_user
POSTGRES_PASSWORD=

# Redis
REDIS_HOST=
REDIS_PORT=
```

### 4. Получение OpenAI API ключа

1. Зарегистрируйтесь на [OpenAI Platform](https://platform.openai.com/)
2. Создайте новый API ключ в разделе API Keys
3. Скопируйте ключ в `.env`

### 5. Запуск с Docker Compose

```bash
# Сборка и запуск всех сервисов
docker-compose up --build
```


## 📝 API Документация

После запуска backend, документация доступна по адресам:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Основные endpoints:

- `GET /health` - Проверка состояния сервиса
- `POST /api/v1/chat` - Отправка сообщения AI агенту
- `DELETE /api/v1/conversations/{user_id}` - Очистка истории разговора
- `GET /api/v1/conversations/{user_id}/history` - Получение истории
- `GET /api/v1/stats` - Статистика использования

## 🤖 Команды бота

- `/start` - Начать работу с ботом
- `/help` - Получить помощь
- `/clear` - Очистить контекст разговора

## 🔧 Конфигурация

### Переменные окружения

| Переменная | Описание | Обязательная |
|------------|----------|--------------|
| `TELEGRAM_TOKEN` | Токен Telegram бота | ✅ |
| `OPENAI_API_KEY` | API ключ OpenAI | ✅ |
| `OPENAI_MODEL` | Модель OpenAI (по умолчанию: gpt-3.5-turbo) | ❌ |
| `DATABASE_URL` | URL подключения к PostgreSQL | ❌ |
| `BACKEND_URL` | URL backend сервиса | ❌ |
| `LOG_LEVEL` | Уровень логирования | ❌ |

## 🐛 Отладка

### Общие проблемы

1. **Бот не отвечает**:
   - Проверьте токен бота
   - Убедитесь, что backend запущен
   - Проверьте логи: `docker-compose logs bot`

2. **Ошибки AI**:
   - Проверьте OpenAI API ключ
   - Убедитесь в наличии средств на счету OpenAI
   - Проверьте лимиты API

3. **Проблемы с базой данных**:
   - Проверьте подключение к PostgreSQL
   - Убедитесь, что миграции выполнены
   - Проверьте логи: `docker-compose logs postgres`


## 📊 Мониторинг

### Метрики

Backend предоставляет следующие метрики:
- Общее количество сообщений
- Уникальные пользователи
- Сообщения за последние 24 часа

### Логирование

Все сервисы ведут структурированные логи:
- Уровень INFO для нормальной работы
- Уровень ERROR для ошибок
- Уровень DEBUG для отладки

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для фичи (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте изменения (`git commit -m 'Add amazing feature'`)
4. Отправьте ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 Лицензия

Этот проект создан для тестового задания.

## 🆘 Поддержка

Если у вас возникли вопросы или проблемы:

1. Проверьте раздел "Отладка" в этом README
2. Просмотрите логи приложения
3. Создайте issue в репозитории с описанием проблемы

---
