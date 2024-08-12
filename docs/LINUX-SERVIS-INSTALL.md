# Установка бота как службы на Linux
_Настройка бота как службы позволяет запускать его в фоновом режиме и легко управлять._

## Шаги установки
#### I. Клонирование репозитория
1. Выберите папку, где будет храниться ваш бот:
    `root/example_folder` _(например)_
2. Откройте терминал и перейдите в эту папку:
    `cd root/example_folder`
3. Клонируйте репозиторий с помощью [git](https://www.git-scm.com/):
    `git clone https://github.com/HiddenCodeDevs/DogsHouseRefBot.git`
4. Перейдите в клонированный репозиторий:
    `cd root/example_folder/DogsHouseRefBot`

#### II. Настройка проекта
1. Создайте виртуальное окружение:
    `python3 -m venv venv`
2. Активируйте виртуальное окружение:
  `source venv/bin/activate`
3. Установите все зависимости Python:
  `pip3 install -r requirements.txt`
4. Создайте файл окружения из шаблона:
  `cp .env-example .env`
5. Настройте необходимые параметры в файле `.env` с помощью любого текстового редактора:
  `nano .env` _(nano в качестве примера)_
6. Запустите `main.py` и инициализируйте сессию.

#### III. Создание службы
1. Перейдите в системную папку, где хранятся все службы, используя терминал:
    `cd /etc/systemd/system/`
2. Создайте файл службы с любым именем:
    `sudo touch DogsHouseRefBot.service`
3. Заполните файл `.service` содержимым, используя любой текстовый редактор:
    `sudo nano DogsHouseRefBot.service` _(nano в качестве примера)_
    **Содержимое:**
    > ```makefile
    > [Unit]
    > Description=DogsHouseRefBotService
    > After=network.target
    > 
    > [Service]
    > User=root
    > WorkingDirectory=/root/example/DogsHouseRefBot/
    > Environment=PATH=/root/example/DogsHouseRefBot/venv/bin/
    > ExecStart=/root/example/DogsHouseRefBot/venv/bin/python3 /root/example/DogsHouseRefBot/main.py -a 2
    > 
    > Restart=always
    > 
    > [Install]
    > WantedBy=multi-user.target
    > ```
 - `User=` - пользователь, от имени которого запускается служба
 - `WorkingDirectory=` - путь к папке с клонированным репозиторием
 - `Environment=` - путь к виртуальному окружению / значение переменной окружения 
 - `ExecStart=` - команда запуска

#### IV. Запуск службы
1. Перезагрузите конфигурацию менеджера служб, используя терминал:
    `sudo systemctl daemon-reload`
1. Включите службу, настроив ее на автоматический запуск:
    `sudo systemctl enable DogsHouseRefBot.service`
___
**Теперь мы закончили.**

___
# Управление службой:
**Остановить службу:**
`sudo systemctl stop DogsHouseRefBot.service`

**Запустить службу:**
`sudo systemctl start DogsHouseRefBot.service`

**Перезапустить службу:**
`sudo systemctl restart DogsHouseRefBot.service`

**Проверить статус:**
`sudo systemctl status DogsHouseRefBot.service`

**Проверить логи:**
`sudo journalctl -u DogsHouseRefBot.service`

**Проверить логи в реальном времени:**
`sudo journalctl -u DogsHouseRefBot.service -f`