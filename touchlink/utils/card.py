from aiohttp import ClientSession, client_exceptions
from attrify import Attrify
from touchlink import config
import ujson as json


async def get_card_balance(card: str):
    async with ClientSession(headers={'content-type': "application/json",'x-rapidapi-host': config.get('bypass', 'host'),'x-rapidapi-key': config.get('bypass', 'api_key')}) as ses:
        async with ses.post(
            config.get('bypass', 'url'),
            data="{\"url\": \"https://bus-transportlink.mtcc.mv/api/card/{}/balance\"}".format(card)
        ) as resp:
            try:
                data = json.loads((await resp.json())["body"])
            except BaseException:
                data = {'success':False,'message': 'Invalid card number'}
    return Attrify(data)
