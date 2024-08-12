import asyncio
from urllib.parse import unquote

from pyrogram import Client
from pyrogram.errors import (
    AuthKeyUnregistered,
    FloodWait,
    Unauthorized,
    UserDeactivated,
)
from pyrogram.raw.functions.messages import RequestAppWebView
from pyrogram.raw.types import InputBotAppShortName
from bot.exceptions import InvalidSession
from bot.utils.logger import logger
from bot.utils.proxy import get_proxy_dict
from bot.config.config import settings


async def get_init_data(
    tg_client: Client, proxy: str | None, session_name: str
):
    proxy_dict = get_proxy_dict(proxy)

    tg_client.proxy = proxy_dict

    try:
        if not tg_client.is_connected:
            try:
                await tg_client.connect()
            except (Unauthorized, UserDeactivated, AuthKeyUnregistered):
                raise InvalidSession(session_name)

        while True:
            try:
                peer = await tg_client.resolve_peer('dogshouse_bot')
                break
            except FloodWait as fl:
                fls = fl.value

                logger.warning(f'{session_name} | FloodWait {fl}')
                fls *= 2
                logger.info(f'{session_name} | Sleep {fls}s')

                await asyncio.sleep(fls)

        bot_app = InputBotAppShortName(bot_id=peer, short_name="join")

        if settings.REFERRAL_TOKEN == "":
            web_view = await tg_client.invoke(
                RequestAppWebView(
                    peer=peer,
                    app=bot_app,
                    platform='android',
                    write_allowed=True
                )
            )
        else:
            web_view = await tg_client.invoke(
                RequestAppWebView(
                    peer=peer,
                    app=bot_app,
                    platform='android',
                    write_allowed=True,
                    start_param=settings.REFERRAL_TOKEN
                )
            )

        auth_url = web_view.url
        tg_web_data = unquote(
            string=auth_url.split('tgWebAppData=', maxsplit=1)[1].split('&tgWebAppVersion', maxsplit=1)[0])

        try:
            information = await tg_client.get_me()
            user_id = information.id
        except Exception as e:
            print(e)

        if tg_client.is_connected:
            await tg_client.disconnect()

        return tg_web_data, user_id

    except InvalidSession as error:
        raise error

    except Exception as error:
        logger.error(
            f'{session_name} | Unknown error during Authorization: {error}'
        )
        await asyncio.sleep(delay=3)
