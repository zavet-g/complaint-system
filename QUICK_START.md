# ⚡ Быстрый старт - Система обработки жалоб

## 🚀 Самый быстрый способ запуска

### 1. Подготовка (30 секунд)
```bash
# Убедитесь что Python 3.8+ установлен
python3 --version

# Сделайте скрипт запуска исполняемым
chmod +x run.sh
```

### 2. Первый запуск (1 минута)
```bash
# Запустите скрипт - он покажет что нужно настроить
./run.sh
```

### 3. Настройка API ключей (5 минут)
Скрипт создаст файл `.env`. Отредактируйте его:

```env
SENTIMENT_API_KEY=ваш_ключ_apilayer
OPENAI_API_KEY=ваш_ключ_openai  
SPAM_API_KEY=ваш_ключ_api_ninjas
```

**Где взять ключи:**
- **APILayer**: https://apilayer.com/marketplace/sentiment-analysis-api (100 запросов/месяц бесплатно)
- **OpenAI**: https://platform.openai.com/api-keys
- **API Ninjas**: https://api-ninjas.com/ (50 запросов/день бесплатно)

### 4. Финальный запуск (30 секунд)
```bash
# Запустите снова
./run.sh
```

## ✅ Проверка работы

```bash
# Проверка здоровья API
curl http://localhost:8000/health/

# Создание тестовой жалобы
curl -X POST "http://localhost:8000/complaints/" \
  -H "Content-Type: application/json" \
  -d '{"text": "Не приходит SMS-код для подтверждения"}'
```

## 🌐 Доступные URL

- **API**: http://localhost:8000
- **Документация**: http://localhost:8000/docs
- **Проверка здоровья**: http://localhost:8000/health/

## 🐳 Альтернативный способ через Docker

```bash
# Настройка
cp env.example .env
nano .env  # добавьте API ключи

# Запуск
docker-compose up --build
```

## 🆘 Если что-то не работает

1. **Python не найден**: Установите Python 3.8+
2. **Порты заняты**: Измените порты в `.env` или остановите другие сервисы
3. **API ключи не работают**: Проверьте правильность ключей и кредиты
4. **Подробная инструкция**: Смотрите `DEPLOYMENT.md`

## 📞 Поддержка

- **Документация API**: http://localhost:8000/docs
- **Подробная инструкция**: `DEPLOYMENT.md`
- **Тестовый скрипт**: `python test_api.py` 