[<img src="https://img.shields.io/badge/Telegram-%40Me-orange">](https://t.me/sho6ot)
[<img src="https://img.shields.io/badge/python-3.10%20%7C%203.11-blue">](https://www.python.org/downloads/)

![img1](.github/images/demo.png)

> 🇷🇺 README на русском доступен [здесь](README.md)

## ⚙ [Settings](https://github.com/shamhi/CoinEggBot/blob/main/.env-example)
| Setting                  | Description                                                               |
|--------------------------|---------------------------------------------------------------------------|
| **API_ID / API_HASH**    | Platform data from which to launch a Telegram session _(stock - Android)_ |
| **REFERRAL_TOKEN**       | Referral token that will activate all sessions _(eg kBNoWEHfEAB1Snb12aP)_ |
| **CLAIM_INVITE_REWARD**  | Whether to claim rewards from invited friends _(True / False)_            |
| **BUY_SCENES**           | Whether to buy new locations _(True / False)_                             |
| **SLEEP_BETWEEN_CLAIM**  | Random delay between claim in seconds _(eg [2,4])_                        |
| **SLEEP_INTERVAL**       | Interval of delay in cycle _(eg 60)_                                      |
| **USE_RANDOM_USERAGENT** | Whether to random User Agent every time to start _(True / False)_         |

## 📕 Профили
Possible to create a profile with unique data for each session:
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
> ❕ **Note**:  `session1` и `session2` - are examples of session names.

## ⚡ Quick Start
1. To install libraries on Windows click on `INSTALL.bat`.
2. To start the bot use `START.bat` (or in console: `python main.py`).

## 📌 Prerequisites
Before you begin, ensure you have the following installed:
- [Python](https://www.python.org/downloads/) version 3.10 or 3.11

## 📃 Getting API Keys
1. Go to [my.telegram.org](https://my.telegram.org) and log in using your phone number.
2. Select **"API development tools"** and fill out the form to register a new application.
3. Note down the `API_ID` and `API_HASH` in `.env` file provided after registering your application.

## 🧱 Installation
You can download [**Repository**](https://github.com/shamhi/CoinEggBot) by cloning it to your system and installing the necessary dependencies:
```shell
~ >>> git clone https://github.com/shamhi/CoinEggBot.git
~ >>> cd CoinEggBot

#Linux
~/CoinEggBot >>> python3 -m venv venv
~/CoinEggBot >>> source venv/bin/activate
~/CoinEggBot >>> pip3 install -r requirements.txt
~/CoinEggBot >>> cp .env-example .env
~/CoinEggBot >>> nano .env # Here you must specify your API_ID and API_HASH , the rest is taken by default
~/CoinEggBot >>> python3 main.py

#Windows
~/CoinEggBot >>> python -m venv venv
~/CoinEggBot >>> venv\Scripts\activate
~/CoinEggBot >>> pip install -r requirements.txt
~/CoinEggBot >>> copy .env-example .env
~/CoinEggBot >>> # Specify your API_ID and API_HASH, the rest is taken by default
~/CoinEggBot >>> python main.py
```
> Installing as a Linux service for running the bot in the background [here](docs/LINUX-SERVIS-INSTALL_EN.md).

⏳ Also for quick launch you can use arguments, for example:
```shell
~/CoinEggBot >>> python3 main.py --action (1/2)
# Or
~/CoinEggBot >>> python3 main.py -a (1/2)

#1 - Create session
#2 - Run clicker
```
