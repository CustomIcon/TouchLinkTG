from aiohttp import ClientSession, client_exceptions
from attrify import Attrify


async def get_stops():
    async with ClientSession() as ses:
        async with ses.get(
            "https://bus-transportlink.mtcc.mv/api/stop"
        ) as resp:
            try:
                data = await resp.json()
            except client_exceptions.ContentTypeError:
                data = {'success':False,'message': 'API down'}
    return Attrify(data)