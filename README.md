# Парсер расписания с использованием Telegram бота

## Описание
Этот проект представляет собой Telegram бота, предназначенного для помощи студентам и преподавателям в получении актуального расписания занятий. Бот автоматически извлекает информацию с веб-сайта университета с использованием Selenium и BeautifulSoup и отправляет её пользователям в Telegram.

## Технологический стек
- Python 3.8+
- Selenium
- BeautifulSoup
- python-telegram-bot
- python-dotenv



## Установка и настройка
Чтобы запустить бота у себя, выполните следующие шаги:

1. Установите Python версии 3.8 или выше.
2. Установите необходимые зависимости:

3. Скачайте соответствующий драйвер для вашего браузера и настройте путь к нему в файле `.env`.
4. Создайте нового бота в Telegram через BotFather и получите токен.
5. Добавьте полученный токен и путь к драйверу в файл `.env`.

### Конфигурация
1. Создайте файл `.env` в корневой директории проекта с следующими переменными:

TELEGRAM_BOT_TOKEN=<ваш_телеграм_токен>
EDGE_DRIVER_PATH=<путь_к_вебдрайверу>

## Использование
Для начала работы с ботом отправьте ему команду `/start` и введите свои учетные данные в формате `логин;пароль`.

## Архитектура
Бот состоит из следующих компонентов:
1. **Selenium WebDriver**: Автоматизированная навигация по веб-сайту для доступа к расписанию.
2. **BeautifulSoup**: Парсинг HTML и извлечение данных о расписании.
3. **Telebot**: Взаимодействие с пользователем через интерфейс Telegram.

## Безопасность
Конфиденциальные данные защищены и хранятся в `.env` файле, который не включается в репозиторий. Регулярное обновление зависимостей помогает предотвращать уязвимости.

## Разработка и анализ проекта
Работа над проектом включала анализ безопасности и производительности, что позволило идентифицировать и устранить основные точки замедления приложения.

## Заключение
Проект демонстрирует успешную реализацию инструмента для автоматизации процесса получения расписания, облегчая пользователю доступ к информации. В будущем планируется дальнейшее улучшение проекта в соответствии с потребностями пользователей и технологическим прогрессом.
ы