import asyncio
from typing import Any

import aiohttp

from bot.api.http import make_request
from bot.utils.logger import logger

async def get_friends_count(
        http_client: aiohttp.ClientSession, user_id: str, reference: str
) -> dict[str, Any] | Any:
    while True:
        response_json = await make_request(
            http_client,
            'GET',
            f'https://api.onetime.dog/frens?user_id={user_id}&reference={reference}',
            'getting Friend Data',
            'getting Friend Data'
        )
        friend_count = response_json.get('count')
        return friend_count


async def get_tasks(
        http_client: aiohttp.ClientSession, user_id: str, reference: str):
    while True:
        response_json = await make_request(
            http_client,
            'GET',
            f'https://api.onetime.dog/tasks?user_id={user_id}&reference={reference}',
            'getting Tasks',
            'getting Tasks'
        )
        return response_json

async def complete_tasks(tasks, http_client, reference, user_id, session_name, tg_client):

    methods = {
        'good-dog': verify_task,
        'send-bone-okx': verify_task,
        'send-bone-binance': verify_task,
        'send-bone-bybit': verify_task,
        'follow-dogs-x': verify_task,
        'notcoin-other-tiers': verify_task,
        'join-blum-tribe': verify_task,
        'subscribe-durov': verify_task,
        'share-story': verify_task,
        'subscribe-dogs': subscribe_channel_and_verify,
        'subscribe-blum': subscribe_channel_and_verify,
        'subscribe-notcoin': subscribe_channel_and_verify,
        'invite-frens': check_and_verify_invite_friends,
        'add-bone-telegram': add_bone_telegram_and_verify,
        'follow-durov-x': verify_task,
        'follow-notcoin-x': verify_task,
        'follow-blum-x': verify_task,
    }

    tasks_not_completed = []

    for task in tasks:
        if not task['complete']:
            slug = task['slug']
            reward = task['reward']
            tasks_not_completed.append((slug, reward))

    for slug, reward in tasks_not_completed:
        if slug in methods:
            await methods[slug](slug, http_client, reference, reward, user_id, session_name, tg_client)

async def verify_task(task, http_client, reference, reward, user_id, session_name, tg_client):
    try:
        url = f'https://api.onetime.dog/tasks/verify?task={task}&user_id={user_id}&reference={reference}'
        async with http_client.post(url) as response:
            if response.status == 200:
                logger.info(
                    f"<light-yellow>{session_name}</light-yellow> | Task '{task}' completed successfully. Reward: {reward}")
            else:
                logger.error(
                    f"<light-yellow>{session_name}</light-yellow> | Failed to verify task {task}, status code: {response.status}")
    except Exception as error:
        logger.error(f"<light-yellow>{session_name}</light-yellow> | Error verifying task {task}: {error}")

async def check_and_verify_invite_friends(slug, http_client, reference, reward, user_id, session_name, tg_client):
    try:
        url = f'https://api.onetime.dog/frens?user_id={user_id}&reference={reference}'
        async with http_client.get(url) as response:
            response_json = await response.json()
            count = response_json.get('count', 0)
            if count >= 5:
                await verify_task(slug, http_client, reference, reward, user_id, session_name, tg_client)
    except Exception as error:
        logger.error(f"<light-yellow>{session_name}</light-yellow> | Error checking friends count: {error}")

async def subscribe_channel_and_verify(slug, http_client, reference, reward, user_id, session_name, tg_client):
    try:
        if not tg_client.is_connected:
            await tg_client.connect()

        channel = None
        if slug == 'subscribe-dogs':
            channel = 'dogs_community'
        elif slug == 'subscribe-blum':
            channel = 'blumcrypto'
        elif slug == 'subscribe-notcoin':
            channel = 'notcoin'

        if channel:
            await tg_client.join_chat(channel)
            await verify_task(slug, http_client, reference, reward, user_id, session_name, tg_client)

            await asyncio.sleep(5)
            await tg_client.leave_chat(channel)
    except Exception as error:
        logger.error(
            f"<light-yellow>{session_name}</light-yellow> | Error subscribing to channel in task '{slug}': {error}")
    finally:
        if tg_client.is_connected:
            await tg_client.disconnect()

async def add_bone_telegram_and_verify(slug, http_client, reference, reward, user_id, session_name, tg_client):
    try:
        if not tg_client.is_connected:
            await tg_client.connect()

        me = await tg_client.get_me()
        first_name = me.first_name

        await tg_client.update_profile(first_name=f"{first_name} 🦴")
        await asyncio.sleep(5)
        await verify_task(slug, http_client, reference, reward, user_id, session_name, tg_client)
        await asyncio.sleep(3)
        await tg_client.update_profile(first_name=first_name)
    except Exception as error:
        logger.error(
            f"<light-yellow>{session_name}</light-yellow> | Error updating profile and verifying task: {error}")
    finally:
        if tg_client.is_connected:
            await tg_client.disconnect()

async def check_friends_task(http_client, user_id, reference, session_name):
    try:
        response_json = await make_request(
            http_client,
            'GET',
            f'https://api.onetime.dog/tasks?user_id={user_id}&reference={reference}',
            'getting Tasks',
            'getting Tasks'
        )
        for task in response_json:
            if task['slug'] == 'invite-frens' and task['complete'] is True:
                return True
            elif task['slug'] == 'invite-frens' and task['complete'] is False:
                return False
    except Exception as e:
        logger.error(
            f"<light_yellow>{session_name}</light-yellow> | Error checking friends task"
        )