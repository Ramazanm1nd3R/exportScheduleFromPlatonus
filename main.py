import telebot
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import logging
import os
import time
from datetime import datetime

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv('укажите путь до .env')
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Настройка WebDriver для Selenium
def setupBrowser():
    edgeOptions = Options()
    edgeOptions.use_chromium = True
    edgeService = Service(executable_path=os.getenv('EDGE_DRIVER_PATH'))
    browser = webdriver.Edge(service=edgeService, options=edgeOptions)
    return browser

# Функция для получения расписания
def fetchSchedule(login, password):
    browser = setupBrowser()
    try:
        browser.get('https://platonus.iitu.edu.kz')
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "login_input")))
        logger.info("Login input found")
        browser.find_element(By.ID, 'login_input').send_keys(login)
        browser.find_element(By.ID, 'pass_input').send_keys(password)
        browser.find_element(By.ID, 'Submit1').click()
        time.sleep(5)

        newButton = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/v7/#/map']")))
        newButton.click()

        time.sleep(3)

        scheduleLink = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "a.link-info.ng-star-inserted[href='/v7/#/schedule/studentView']"))
        )
        scheduleLink.click()

        logger.info("Waiting for the schedule page to load...")
        time.sleep(5)  # Задержка для полной загрузки страницы расписания

        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Получаем текущий день недели
        todayDayName = datetime.now().strftime('%A')
        # Словарь для перевода английских названий в русские
        dayNameTranslation = {
            'Monday': 'Понедельник',
            'Tuesday': 'Вторник',
            'Wednesday': 'Среда',
            'Thursday': 'Четверг',
            'Friday': 'Пятница',
            'Saturday': 'Суббота',
            'Sunday': 'Воскресенье'
        }
        todayDayNameRu = dayNameTranslation[todayDayName]

        scheduleText = f"Ваше расписание на сегодня ({todayDayNameRu}):\n"

        daySchedule = soup.find('h5', string=todayDayNameRu).find_next_sibling('div', class_='table-responsive')

        if daySchedule:
            rows = daySchedule.find_all('tr', class_='ng-star-inserted')
            for row in rows:
                timeSlot = row.find('td', style='width: 20%;').text.strip()
                lessonDescription = row.find('div', class_='ng-star-inserted').text.strip()
                # Проверяем, есть ли описание урока
                if lessonDescription and not lessonDescription.isspace():
                    scheduleText += f"{timeSlot}: {lessonDescription}\n"
                # Если описание урока отсутствует или состоит только из пробелов, мы пропускаем добавление в расписание
            if not any(row.find('div', class_='ng-star-inserted').text.strip() for row in rows):
                scheduleText = f"На {todayDayNameRu} занятий нет."
        else:
            scheduleText = "Расписание на сегодня не найдено или не может быть прочитано."

        return scheduleText
    except Exception as e:
        logger.error(f"Ошибка при получении расписания: {e}")
        return "Не удалось получить расписание."
    finally:
        browser.quit()

# Обработчики сообщений бота
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Привет! Пожалуйста, отправьте ваш логин и пароль от Platonus в формате: логин;пароль')


@bot.message_handler(func=lambda message: True)
def handleCredentials(message):
    credentials = message.text.split(';')
    if len(credentials) != 2:
        bot.reply_to(message, "Пожалуйста, используйте формат: логин;пароль")
        return
    login, password = credentials
    scheduleText = fetchSchedule(login, password)
    bot.send_message(message.chat.id, scheduleText)


if __name__ == '__main__':
    bot.polling(non_stop=True)
