[<img src="https://img.shields.io/badge/Telegram-%40Me-orange">](https://t.me/unknxwnplxya)
[<img src="https://img.shields.io/badge/python-3.10%20%7C%203.11-blue">](https://www.python.org/downloads/)

![img1](.github/images/demo.png)

> 🇪🇳 README in english available [here](README-EN.md)

## ⚙ [Настройки](https://github.com/HiddenCodeDevs/DogsHouseRefBot/blob/main/.env-example)
| Настройка                | Описание                                                                                   |
|--------------------------|--------------------------------------------------------------------------------------------|
| **API_ID / API_HASH**    | Данные платформы, с которой запускать сессию Telegram _(сток - Android)_                   |
| **REFERRAL_TOKEN**       | Реферальный токен, по которому будут активированы все сессии _(напр. kBNoWEHfEAB1Snb12aP)_ |
| **USE_RANDOM_USERAGENT** | Использовать ли рандомный User Agent при каждом новом запуске _(True / False)_             |

## 📕 Профили
Для каждой сессии можно создать профиль с уникальными данными:
```json
{
  "session1": {
    "proxy": "socks5://yGow3a:uBro3wL@58.195.21.83:9715",
    "headers": {"...": "..."}
  },
  "session2": {
    "proxy": "socks5://yGow3a:uBro3wL@58.195.21.83:9715",
    "headers": {"...": "..."}
  },
  "...": {}
}
```
> ❕ **Примечание**:  `session1` и `session2` - это примеры названий сессий.

## ⚡ Быстрый старт
1. Чтобы установить библиотеки в Windows, запустите INSTALL.bat.
2. Для запуска бота используйте `START.bat` (или в консоли: `python main.py`).

## 📌 Предварительные условия
Прежде чем начать, убедитесь, что у вас установлено следующее:
- [Python](https://www.python.org/downloads/) версии 3.10 или 3.11.

## 📃 Получение API ключей
1. Перейдите на сайт [my.telegram.org](https://my.telegram.org) и войдите в систему, используя свой номер телефона.
2. Выберите **"API development tools"** и заполните форму для регистрации нового приложения.
3. Запишите `API_ID` и `API_HASH` в файле `.env`, предоставленные после регистрации вашего приложения.

## 🧱 Установка
Вы можете скачать [**Репозиторий**](https://github.com/HiddenCodeDevs/DogsHouseRefBot) клонированием на вашу систему и установкой необходимых зависимостей:
```shell
~ >>> git clone https://github.com/HiddenCodeDevs/DogsHouseRefBot.git 
~ >>> cd DogsHouseRefBot

# Linux
~/DogsHouseRefBot >>> python3 -m venv venv
~/DogsHouseRefBot >>> source venv/bin/activate
~/DogsHouseRefBot >>> pip3 install -r requirements.txt
~/DogsHouseRefBot >>> cp .env-example .env
~/DogsHouseRefBot >>> nano .env  # Здесь вы обязательно должны указать ваши API_ID и API_HASH , остальное берется по умолчанию
~/DogsHouseRefBot >>> python3 main.py

# Windows
~/DogsHouseRefBot >>> python -m venv venv
~/DogsHouseRefBot >>> venv\Scripts\activate
~/DogsHouseRefBot >>> pip install -r requirements.txt
~/DogsHouseRefBot >>> copy .env-example .env
~/DogsHouseRefBot >>> # Указываете ваши API_ID и API_HASH, остальное берется по умолчанию
~/DogsHouseRefBot >>> python main.py
```
> Установка в качестве Linux службы для фоновой работы бота [тут](docs/LINUX-SERVIS-INSTALL.md).

⏳ Также для быстрого запуска вы можете использовать аргументы, например:
```shell
~/DogsHouseRefBot >>> python3 main.py --action (1/2)
# Или
~/DogsHouseRefBot >>> python3 main.py -a (1/2)

# 1 - Создает сессию
# 2 - Запускает кликер
```
