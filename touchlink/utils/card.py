from aiohttp import ClientSession, client_exceptions
from attrify import Attrify


async def get_card_balance(card: str):
    async with ClientSession() as ses:
        async with ses.get(
            f"https://bus-transportlink.mtcc.mv/api/card/{card}/balance"
        ) as resp:
            try:
                data = await resp.json()
            except client_exceptions.ContentTypeError:
                data = {'success':False,'message': 'Invalid card number'}
    return Attrify(data)
