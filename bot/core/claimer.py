import asyncio

import aiohttp
from aiohttp_proxy import ProxyConnector
from pyrogram import Client

from bot.config import settings
from bot.utils.logger import logger
from bot.utils.scripts import save_referral_link
from bot.exceptions import InvalidSession
from bot.api.auth import login
from bot.utils.scripts import get_headers
from bot.utils.init_data import get_init_data
from bot.api.clicker import get_friends_count, get_tasks, complete_tasks
from bot.utils.proxy import check_proxy


class Claimer:
    def __init__(self, tg_client: Client):
        self.session_name = tg_client.name
        self.tg_client = tg_client
        self.user_id = None
        self.reference = None

    async def run(self, proxy: str | None) -> None:
        headers = get_headers(name=self.tg_client.name)

        proxy_conn = ProxyConnector().from_url(proxy) if proxy else None

        async with (aiohttp.ClientSession(headers=headers, connector=proxy_conn) as http_client):
            if proxy:
                await check_proxy(
                    http_client=http_client,
                    proxy=proxy,
                    session_name=self.session_name,
                )

            init_data, user_id = await get_init_data(
                tg_client=self.tg_client,
                proxy=proxy,
                session_name=self.session_name
            )

            if not init_data:
                return

            self.user_id = user_id

            while True:
                try:
                    login_json = await login(
                        http_client=http_client,
                        init_data=init_data,
                        referrer=settings.REFERRAL_TOKEN
                    )

                    if not login_json:
                        continue

                    self.reference = login_json['reference']

                    tasks = await get_tasks(
                        http_client=http_client,
                        user_id=self.user_id,
                        reference=self.reference
                    )

                    if tasks:
                        await complete_tasks(tasks, http_client, reference=self.reference, user_id=self.user_id,
                                             session_name=self.session_name, tg_client=self.tg_client)

                    invite_link = f'https://t.me/dogshouse_bot/join?startapp={login_json["reference"]}'

                    count = await get_friends_count(http_client=http_client, user_id=user_id,
                                                    reference=login_json["reference"])
                    if count == 0:
                        save_referral_link(name=self.session_name, referral_link=invite_link,
                                           invite_count=count)

                        logger.success(f'{self.session_name} | saved ref')
                    else:
                        logger.info(f'{self.session_name} | More then zero friends invited, skip saving')

                    await asyncio.sleep(99999)

                except InvalidSession as error:
                    raise error

                except Exception as error:
                    logger.error(f"{self.session_name} | Unknown error: {error}")
                    await asyncio.sleep(delay=3)

async def run_claimer(tg_client: Client, proxy: str | None):
    try:
        await Claimer(tg_client=tg_client).run(proxy=proxy)
    except InvalidSession:
        logger.error(f'{tg_client.name} | Invalid Session')
