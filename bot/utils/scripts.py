import os
import glob
import random

from fake_useragent import UserAgent

from bot.config import settings
from bot.utils.json_db import JsonDB
from bot.utils.default import DEFAULT_HEADERS


def get_session_names():
    names = [os.path.splitext(os.path.basename(file))[0] for file in glob.glob('sessions/*.session')]

    return names


def escape_html(text: str):
    return text.replace('<', '\\<').replace('>', '\\>')


def save_referral_link(name: str, referral_link: str, invite_count: int):
    db = JsonDB("referrals")

    referrals = db.get_data()
    referrals[name] = {
        'link': referral_link,
        'count': invite_count
    }

    db.save_data(referrals)

def save_balance(name: str, balance_value: int, withdraw, wallet):
    db = JsonDB("accounts_balance")

    accounts_balance = db.get_data()
    accounts_balance[name] = {
        'balance': balance_value,
        'withdraw_status': withdraw,
        'wallet': wallet
    }

    db.save_data(accounts_balance)


def get_headers(name: str):
    db = JsonDB("profiles")

    profiles = db.get_data()

    headers = profiles.get(name, {}).get('headers', DEFAULT_HEADERS)

    if settings.USE_RANDOM_USERAGENT:
        android_version = random.randint(24, 33)
        webview_version = random.randint(70, 125)

        headers['Sec-Ch-Ua'] = (
            f'"Android WebView";v="{webview_version}", '
            f'"Chromium";v="{webview_version}", '
            f'"Not?A_Brand";v="{android_version}"'
        )
        headers['User-Agent'] = get_mobile_user_agent()

    return headers


def get_mobile_user_agent() -> str:
    """
    Function: get_mobile_user_agent

    This method generates a random mobile user agent for an Android platform.
    If the generated user agent does not contain the "wv" string,
    it adds it to the browser version component.

    :return: A random mobile user agent for Android platform.
    """
    ua = UserAgent(platforms=['mobile'], os=['android'])
    user_agent = ua.random
    if 'wv' not in user_agent:
        parts = user_agent.split(')')
        parts[0] += '; wv'
        user_agent = ')'.join(parts)
    return user_agent
