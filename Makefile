# Makefile для системы обработки жалоб

.PHONY: help install run test clean docker-build docker-run

# Переменные
PYTHON = python3
PIP = pip3
APP_NAME = complaint-system
PORT = 8000

help: ## Показать справку
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Установить зависимости
	$(PIP) install -r requirements.txt

run: ## Запустить приложение
	$(PYTHON) main.py

dev: ## Запустить в режиме разработки
	uvicorn main:app --reload --host 0.0.0.0 --port $(PORT)

test: ## Запустить все тесты
	$(PYTHON) tests/run_all_tests.py

test-api: ## Запустить API тесты
	$(PYTHON) tests/api/test_api.py

test-unit: ## Запустить модульные тесты
	$(PYTHON) tests/unit/test_telegram.py
	$(PYTHON) tests/unit/test_google_sheets.py

test-integration: ## Запустить интеграционные тесты
	$(PYTHON) tests/integration/test_integration.py

pytest: ## Запустить тесты с pytest
	pytest tests/ -v

clean: ## Очистить временные файлы
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

docker-build: ## Собрать Docker образ
	docker build -t $(APP_NAME) .

docker-run: ## Запустить в Docker
	docker-compose up --build

docker-stop: ## Остановить Docker контейнеры
	docker-compose down

logs: ## Показать логи
	docker-compose logs -f

setup: ## Первоначальная настройка
	@echo "Настройка системы обработки жалоб..."
	@if [ ! -f .env ]; then cp env.example .env; echo "Создан файл .env из env.example"; fi
	@chmod +x run.sh
	@echo "Установка зависимостей..."
	$(MAKE) install
	@echo "Настройка завершена! Отредактируйте .env файл и запустите: make run"

health: ## Проверить здоровье API
	curl http://localhost:$(PORT)/health/

create-complaint: ## Создать тестовую жалобу
	curl -X POST "http://localhost:$(PORT)/complaints/" \
		-H "Content-Type: application/json" \
		-d '{"text": "Тестовая жалоба - сайт не работает"}'

list-complaints: ## Получить список жалоб
	curl http://localhost:$(PORT)/complaints/

telegram-test: ## Тест Telegram уведомлений
	curl -X POST "http://localhost:$(PORT)/telegram/test/"

sheets-test: ## Тест Google Sheets
	curl -X POST "http://localhost:$(PORT)/sheets/setup/"
	curl http://localhost:$(PORT)/sheets/summary/ 