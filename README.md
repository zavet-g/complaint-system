# 🤖 Complaint System — AI-powered Customer Complaint Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?logo=openai&logoColor=white)](https://openai.com/)
[![Telegram](https://img.shields.io/badge/Telegram-26A5E4?logo=telegram&logoColor=white)](https://telegram.org/)
[![Google Sheets](https://img.shields.io/badge/Google%20Sheets-34A853?logo=google-sheets&logoColor=white)](https://www.google.com/sheets/about/)
[![Tests](https://img.shields.io/badge/Tests-passing-brightgreen)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Описание

**Complaint System** — это современная система обработки жалоб клиентов с поддержкой искусственного интеллекта:  
- автоматическая категоризация обращений  
- анализ тональности  
- уведомления в реальном времени  
- интеграция с Telegram, Google Sheets и OpenAI  
- готова к продакшену, поддерживает Docker и комплексное тестирование

---

## 🚀 Возможности

- Создание и управление жалобами через REST API
- AI-категоризация с fallback на ключевые слова
- Анализ тональности (русский и английский)
- Уведомления в Telegram (при настройке)
- Экспорт в Google Sheets (при настройке)
- Полный набор тестов
- Docker поддержка
- Автоматическая документация API (Swagger/OpenAPI)
- Health checks, логирование, валидация данных

---

## 🛠️ Технологический стек

- **FastAPI** — современный асинхронный веб-фреймворк
- **SQLAlchemy 2.0** — ORM для работы с БД
- **Pydantic** — валидация и сериализация данных
- **httpx** — асинхронные HTTP-запросы
- **python-dotenv** — управление переменными окружения
- **pytest** — тестирование
- **Docker** — контейнеризация
- **n8n** — автоматизация процессов

---

## 📦 Внешние сервисы

- **OpenAI GPT-3.5 Turbo** — AI-категоризация жалоб
- **APILayer Sentiment Analysis** — анализ тональности
- **API Ninjas Spam Check** — проверка на спам
- **IP API** — геолокация по IP
- **Telegram Bot API** — уведомления
- **Google Sheets API** — экспорт данных

---

## 📁 Структура проекта

```
complaint-system/
├── app/
│   ├── config.py
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── utils/
├── docs/
│   ├── QUICK_START.md
│   ├── DEPLOYMENT.md
│   ├── TESTING.md
│   ├── TELEGRAM_SETUP.md
│   ├── GOOGLE_SHEETS_SETUP.md
│   ├── n8n_setup.md
│   └── PROJECT_SUMMARY.md
├── tests/
│   ├── api/
│   ├── integration/
│   ├── unit/
│   └── run_all_tests.py
├── main.py
├── database.py
├── models.py
├── services.py
├── requirements.txt
├── env.example
├── run.sh
├── Makefile
├── docker-compose.yml
├── Dockerfile
├── n8n_workflow.json
└── README.md
```

---

## ⚡ Быстрый старт

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/zavet-g/complaint-system.git
   cd complaint-system
   ```

2. **Создайте и настройте `.env` файл:**
   ```bash
   cp env.example .env
   # Заполните переменные окружения
   ```

3. **Установите зависимости:**
   ```bash
   make install
   ```

4. **Запустите сервер:**
   ```bash
   make run
   # или в Docker
   make docker-run
   ```

5. **Откройте документацию API:**
   - [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Тестирование

- Запустить все тесты:
  ```bash
  make test
  ```
- Запустить отдельные группы тестов:
  ```bash
  make test-api
  make test-unit
  make test-integration
  ```

---

## 📝 Документация

- [Быстрый старт](docs/QUICK_START.md)
- [Развёртывание](docs/DEPLOYMENT.md)
- [Тестирование](docs/TESTING.md)
- [Настройка Telegram](docs/TELEGRAM_SETUP.md)
- [Настройка Google Sheets](docs/GOOGLE_SHEETS_SETUP.md)
- [Настройка n8n](docs/n8n_setup.md)
- [Обзор проекта](docs/PROJECT_SUMMARY.md)

---

## 🤝 Вклад в проект

1. Сделайте fork репозитория
2. Создайте ветку (`git checkout -b feature/your-feature`)
3. Commit изменения (`git commit -m 'Add your feature'`)
4. Push в ветку (`git push origin feature/your-feature`)
5. Откройте Pull Request

---

## 📄 Лицензия

Проект распространяется под лицензией MIT. Подробнее см. в файле [LICENSE](LICENSE).

---

## 👤 Автор и связь

**Артём Букарев**  
Telegram: [@bcdbcddd](https://t.me/bcdbcddd)  
GitHub: [zavet-g/complaint-system](https://github.com/zavet-g/complaint-system)

---

## ⭐️ Поддержите проект!

Если проект был полезен — поставьте ⭐️ на [GitHub](https://github.com/zavet-g/complaint-system)! 