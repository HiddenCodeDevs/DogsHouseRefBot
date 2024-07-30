import asyncio
import string
import sys
import random

import aiohttp
import json

from aiocfscrape import CloudflareScraper
from aiohttp_proxy import ProxyConnector
from better_proxy import Proxy
from urllib.parse import unquote, quote

from faker import Faker
from pyrogram import Client
from pyrogram.errors import Unauthorized, UserDeactivated, AuthKeyUnregistered, FloodWait
from pyrogram.raw.functions.messages import RequestAppWebView
from pyrogram.raw import types

from bot.config import settings
from bot.utils import logger
from bot.exceptions import InvalidSession

from .headers import headers
from .agents import generate_random_user_agent


class Tapper:
    def __init__(self, tg_client: Client):
        self.session_name = tg_client.name
        self.tg_client = tg_client
        self.user_id = 0
        self.username = None
        self.start_param = None
        self.url = 'https://api.onetime.dog'

        self.session_ug_dict = self.load_user_agents() or []

        headers['User-Agent'] = self.check_user_agent()

    async def generate_random_user_agent(self):
        return generate_random_user_agent(device_type='android', browser_type='chrome')

    def save_user_agent(self):
        user_agents_file_name = "user_agents.json"

        if not any(session['session_name'] == self.session_name for session in self.session_ug_dict):
            user_agent_str = generate_random_user_agent()

            self.session_ug_dict.append({
                'session_name': self.session_name,
                'user_agent': user_agent_str})

            with open(user_agents_file_name, 'w') as user_agents:
                json.dump(self.session_ug_dict, user_agents, indent=4)

            logger.success(f"<light-yellow>{self.session_name}</light-yellow> | User agent saved successfully")

            return user_agent_str

    def load_user_agents(self):
        user_agents_file_name = "user_agents.json"

        try:
            with open(user_agents_file_name, 'r') as user_agents:
                session_data = json.load(user_agents)
                if isinstance(session_data, list):
                    return session_data

        except FileNotFoundError:
            logger.warning("User agents file not found, creating...")

        except json.JSONDecodeError:
            logger.warning("User agents file is empty or corrupted.")

        return []

    def check_user_agent(self):
        load = next(
            (session['user_agent'] for session in self.session_ug_dict if session['session_name'] == self.session_name),
            None)

        if load is None:
            return self.save_user_agent()

        return load

    async def get_tg_web_data(self, proxy: str | None, http_client: aiohttp.ClientSession) -> str:
        if proxy:
            proxy = Proxy.from_str(proxy)
            proxy_dict = dict(
                scheme=proxy.protocol,
                hostname=proxy.host,
                port=proxy.port,
                username=proxy.login,
                password=proxy.password
            )
        else:
            proxy_dict = None

        self.tg_client.proxy = proxy_dict

        try:
            with_tg = True

            if not self.tg_client.is_connected:
                with_tg = False
                try:
                    await self.tg_client.connect()
                except (Unauthorized, UserDeactivated, AuthKeyUnregistered):
                    raise InvalidSession(self.session_name)

            while True:
                try:
                    peer = await self.tg_client.resolve_peer('dogshouse_bot')
                    break
                except FloodWait as fl:
                    fls = fl.value

                    logger.warning(f"{self.session_name} | FloodWait {fl}")
                    logger.info(f"{self.session_name} | Sleep {fls}s")

                    await asyncio.sleep(fls + 3)

            InputBotApp = types.InputBotAppShortName(bot_id=peer, short_name="join")

            if settings.REF_ID == '':
                logger.critical('PLEASE ENTER REF ARGUMENT (AFTER STARTAPP?= TEXT) ((YOU CAN PUT UR REFERRAL, '
                                'OTHERWISE BOT WONT WORK))')
                await http_client.close()
                await self.tg_client.disconnect()
                sys.exit()
            else:
                start_param = settings.REF_ID
                self.start_param = start_param

            web_view = await self.tg_client.invoke(RequestAppWebView(
                peer=peer,
                app=InputBotApp,
                platform='android',
                write_allowed=True,
                start_param=start_param,
            ))

            auth_url = web_view.url
            tg_web_data = unquote(
                string=unquote(
                    string=auth_url.split('tgWebAppData=', maxsplit=1)[1].split('&tgWebAppVersion', maxsplit=1)[0]))

            me = await self.tg_client.get_me()
            self.user_id = me.id
            self.username = me.username if me.username else ''
            if self.username == '':
                while True:
                    fake = Faker('en_US')

                    name_english = fake.name()
                    name_modified = name_english.replace(" ", "").lower()

                    random_letters = ''.join(random.choices(string.ascii_lowercase, k=random.randint(1, 7)))
                    final_name = name_modified + random_letters
                    status = await self.tg_client.set_username(final_name)
                    if status:
                        logger.info(f"{self.session_name} | Set username {final_name}")
                        break
                    else:
                        continue

            if with_tg is False:
                await self.tg_client.disconnect()

            return tg_web_data

        except InvalidSession as error:
            raise error

        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error during Authorization: {error}")
            await asyncio.sleep(delay=3)

    async def join_request(self, http_client: aiohttp.ClientSession, init_data):
        try:
            response = await http_client.post(url=f'https://api.onetime.dog/join?invite_hash={self.start_param}',
                                              data=init_data)
            if response.status not in (200, 201):
                return False, None, None, None
            response_json = await response.json()
            balance = response_json.get('balance')
            reference = response_json.get('reference')
            streak = response_json.get('streak')
            return (True,
                    balance,
                    reference,
                    streak)
        except Exception as error:
            logger.error(f"<light-yellow>{self.session_name}</light-yellow> | Join request error - {error}")

    async def check_proxy(self, http_client: aiohttp.ClientSession, proxy: Proxy) -> None:
        try:
            response = await http_client.get(url='https://httpbin.org/ip', timeout=aiohttp.ClientTimeout(5))
            ip = (await response.json()).get('origin')
            logger.info(f"{self.session_name} | Proxy IP: {ip}")
        except Exception as error:
            logger.error(f"{self.session_name} | Proxy: {proxy} | Error: {error}")

    async def get_reference(self, http_client, proxy, reference):
        if reference is None:

            asyncio.sleep(5)

            tg_web_data = await self.get_tg_web_data(proxy=proxy, http_client=http_client)
            tg_web_data_parts = tg_web_data.split('&')

            user_data = tg_web_data_parts[0].split('=')[1]
            chat_instance = tg_web_data_parts[1].split('=')[1]
            chat_type = tg_web_data_parts[2].split('=')[1]
            start_param = tg_web_data_parts[3].split('=')[1]
            auth_date = tg_web_data_parts[4].split('=')[1]
            hash_value = tg_web_data_parts[5].split('=')[1]

            user_data_encoded = quote(user_data)

            init_data = (f"user={user_data_encoded}&chat_instance={chat_instance}&chat_type={chat_type}&"
                         f"start_param={start_param}&auth_date={auth_date}&hash={hash_value}")

            status, balance, new_reference, streak = await self.join_request(http_client=http_client,
                                                                             init_data=init_data)
            if not status:
                logger.error(
                    f"<light-yellow>{self.session_name}</light-yellow> | Failed to obtain reference from join_request.")
                return None
            return new_reference
        return reference

    async def get_tasks(self, http_client, proxy, reference):
        try:
            reference = await self.get_reference(http_client=http_client, proxy=proxy, reference=reference)
            if reference is None:
                return None

            response = await http_client.get(url=f'{self.url}/tasks?user_id={self.user_id}&reference={reference}')
            response_json = await response.json()
            return response_json

        except Exception as error:
            logger.error(f"<light-yellow>{self.session_name}</light-yellow> | Get tasks request error - {error}")
            return None

    async def complete_tasks(self, tasks, http_client, proxy, reference):
        if not tasks:
            logger.info(f"<light-yellow>{self.session_name}</light-yellow> | No tasks found or error occurred")
            return

        reference = await self.get_reference(http_client=http_client, proxy=proxy, reference=reference)
        if reference is None:
            return

        methods = {
            'good-dog': self.verify_task,
            'send-bone-okx': self.verify_task,
            'send-bone-binance': self.verify_task,
            'send-bone-bybit': self.verify_task,
            'follow-dogs-x': self.verify_task,
            'notcoin-other-tiers': self.verify_task,
            'join-blum-tribe': self.verify_task,
            'subscribe-durov': self.verify_task,
            'subscribe-dogs': self.subscribe_channel_and_verify,
            'subscribe-blum': self.subscribe_channel_and_verify,
            'subscribe-notcoin': self.subscribe_channel_and_verify,
            'invite-frens': self.check_and_verify_invite_friends,
            'add-bone-telegram': self.add_bone_telegram_and_verify,
        }

        tasks_not_completed = []

        for task in tasks:
            if not task['complete']:
                slug = task['slug']
                reward = task['reward']
                tasks_not_completed.append((slug, reward))

        for slug, reward in tasks_not_completed:
            if slug in methods:
                await methods[slug](slug, http_client, reference, reward)

    async def verify_task(self, task, http_client, reference, reward):
        try:
            url = f'{self.url}/tasks/verify?task={task}&user_id={self.user_id}&reference={reference}'
            async with http_client.post(url) as response:
                if response.status == 200:
                    logger.info(
                        f"<light-yellow>{self.session_name}</light-yellow> | Task '{task}' completed successfully. Reward: {reward}")
                else:
                    logger.error(
                        f"<light-yellow>{self.session_name}</light-yellow> | Failed to verify task {task}, status code: {response.status}")
        except Exception as error:
            logger.error(f"<light-yellow>{self.session_name}</light-yellow> | Error verifying task {task}: {error}")

    async def check_and_verify_invite_friends(self, slug, http_client, reference, reward):
        try:
            url = f'{self.url}/frens?user_id={self.user_id}&reference={reference}'
            async with http_client.get(url) as response:
                response_json = await response.json()
                count = response_json.get('count', 0)
                if count >= 5:
                    await self.verify_task(slug, http_client, reference, reward)
        except Exception as error:
            logger.error(f"<light-yellow>{self.session_name}</light-yellow> | Error checking friends count: {error}")

    async def subscribe_channel_and_verify(self, slug, http_client, reference, reward):
        try:
            if not self.tg_client.is_connected:
                await self.tg_client.connect()

            channel = None
            if slug == 'subscribe-dogs':
                channel = 'dogs_community'
            elif slug == 'subscribe-blum':
                channel = 'blumcrypto'
            elif slug == 'subscribe-notcoin':
                channel = 'notcoin'

            if channel:
                await self.tg_client.join_chat(channel)
                await self.verify_task(slug, http_client, reference, reward)

                await asyncio.sleep(5)
                await self.tg_client.leave_chat(channel)
        except Exception as error:
            logger.error(
                f"<light-yellow>{self.session_name}</light-yellow> | Error subscribing to channel in task '{slug}': {error}")
        finally:
            if self.tg_client.is_connected:
                await self.tg_client.disconnect()

    async def add_bone_telegram_and_verify(self, slug, http_client, reference, reward):
        try:
            if not self.tg_client.is_connected:
                await self.tg_client.connect()

            me = await self.tg_client.get_me()
            first_name = me.first_name

            await self.tg_client.update_profile(first_name=f"{first_name} 🦴")
            await asyncio.sleep(5)
            await self.verify_task(slug, http_client, reference, reward)
            await asyncio.sleep(3)
            await self.tg_client.update_profile(first_name=first_name)
        except Exception as error:
            logger.error(
                f"<light-yellow>{self.session_name}</light-yellow> | Error updating profile and verifying task: {error}")
        finally:
            if self.tg_client.is_connected:
                await self.tg_client.disconnect()

    async def run(self, proxy: str | None) -> None:
        proxy_conn = ProxyConnector().from_url(proxy) if proxy else None

        http_client = CloudflareScraper(headers=headers, connector=proxy_conn)

        if proxy:
            await self.check_proxy(http_client=http_client, proxy=proxy)

        first_run = True
        streak_daily = 0
        referred = False

        while True:
            try:
                tg_web_data = await self.get_tg_web_data(proxy=proxy, http_client=http_client)
                tg_web_data_parts = tg_web_data.split('&')

                user_data = tg_web_data_parts[0].split('=')[1]
                chat_instance = tg_web_data_parts[1].split('=')[1]
                chat_type = tg_web_data_parts[2].split('=')[1]
                start_param = tg_web_data_parts[3].split('=')[1]
                auth_date = tg_web_data_parts[4].split('=')[1]
                hash_value = tg_web_data_parts[5].split('=')[1]

                user_data_encoded = quote(user_data)

                init_data = (f"user={user_data_encoded}&chat_instance={chat_instance}&chat_type={chat_type}&"
                             f"start_param={start_param}&auth_date={auth_date}&hash={hash_value}")

                status, balance, reference, streak = await self.join_request(http_client=http_client,
                                                                             init_data=init_data)

                if streak_daily != streak:
                    streak_daily = streak
                    if first_run:
                        logger.success(f"<light-yellow>{self.session_name}</light-yellow> | Successfully remembered "
                                       f"streak and maybe get it (first run)")
                    else:
                        logger.success(f"<light-yellow>{self.session_name}</light-yellow> | Successfully got new streak"
                                       f", now {streak_daily}")

                if status and not referred:
                    logger.info(f"<light-yellow>{self.session_name}</light-yellow> | Successfully logged and referral, "
                                f"balance: {balance}")
                    referred = True

                if settings.AUTO_TASKS:
                    tasks = await self.get_tasks(http_client=http_client, proxy=proxy, reference=reference)
                    if tasks:
                        await self.complete_tasks(tasks, http_client=http_client, proxy=proxy, reference=reference)

                logger.info(f"<light-yellow>{self.session_name}</light-yellow> | Going sleep 12h")

                await asyncio.sleep(12 * 3600)

            except InvalidSession as error:
                raise error

            except Exception as error:
                logger.error(f"{self.session_name} | Unknown error: {error}")
                await asyncio.sleep(delay=3)


async def run_tapper(tg_client: Client, proxy: str | None):
    try:
        await Tapper(tg_client=tg_client).run(proxy=proxy)
    except InvalidSession:
        logger.error(f"{tg_client.name} | Invalid Session")
