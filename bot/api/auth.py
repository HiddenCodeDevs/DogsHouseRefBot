import aiohttp

from bot.api.http import handle_error, make_request


async def login(
    http_client: aiohttp.ClientSession, init_data: str, referrer: str = ""
):
    try:
        if referrer == "":
            url = 'https://api.onetime.dog/join'
        else:
            url = f'https://api.onetime.dog/join?invite_hash={referrer}'
        response_json = await make_request(
            http_client,
            'POST',
            url,
            init_data,
            'getting Access Token',
        )
        login_data = response_json
        return login_data
    except Exception as error:
        await handle_error(error, '', 'getting Access Token')
        return None
