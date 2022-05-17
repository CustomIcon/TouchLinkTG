from subprocess import call
from pyrogram import Client, filters, types
from touchlink import database
from tinydb import Query
from pyrogram import emoji
from aiohttp import ClientSession, client_exceptions
from attrify import Attrify
from touchlink.utils import card


@Client.on_callback_query(filters.regex('^get_*'))
async def _(_, query):
    User = Query()
    data = query.data.split('_')
    if data[1] == 'started':
        if not database.search(User.user_id == query.from_user.id):
            database.insert({'user_id': query.from_user.id, 'locale': 'en_US', 'card': 0})
        return await query.message.edit_text(
            "What would you like me to do?",
            reply_markup=types.InlineKeyboardMarkup(
                [
                    [types.InlineKeyboardButton(f'{emoji.MONEY_BAG} Check Balance', callback_data='get_balance')],
                    [types.InlineKeyboardButton(f'{emoji.WOMAN_FACTORY_WORKER} Find Card Agency', callback_data='get_agency')],
                    [types.InlineKeyboardButton(f'{emoji.BUS_STOP} Find a Bus Stop', callback_data='get_stop')],
                    [types.InlineKeyboardButton(
                        f'{emoji.FLAG_UNITED_STATES if User.locale == "en_US" else emoji.FLAG_MALDIVES} Change Language',
                        callback_data='set_language'
                    )],
                ]
            )
        )
    elif data[1] == 'balance':
        if database.search(User.card == 0):
            return await query.message.edit_text(
                "You don't have any cards yet.\nFeel free to add one by pressing the button below.",
                reply_markup=types.InlineKeyboardMarkup(
                    [
                        [types.InlineKeyboardButton(f'{emoji.CREDIT_CARD} Add Card', callback_data='set_card')],
                    ]
                )
            )
        user = database.search(User.user_id == query.from_user.id)
        data = card.get_card_balance(user[0]['card'])
        if data.success:
            return await query.answer(f"{emoji.CREDIT_CARD} Your balance is: {data.data.Balance}", show_alert=True)
    elif data[1] == 'agency':
        async with ClientSession() as ses:
            async with ses.get(
                "https://bus-transportlink.mtcc.mv/api/agents"
            ) as resp:
                data = await resp.json()
        data = Attrify(data)
        if data.success:
            string = ''
            for agency in data.data:
                if agency.url:
                    string += f"{emoji.BUS_STOP} [{agency.name}]({agency.url})\n"
                else:
                    string += f"{emoji.BUS_STOP} {agency.name}\n"
                string += f"island: __{agency.island}__\n\n"
            return await query.message.edit_text(string, disable_web_page_preview=True, reply_markup=types.InlineKeyboardMarkup([[types.InlineKeyboardButton('Back', callback_data='get_started')]]))
    elif data[1] == 'stop':
        return await query.message.edit_text('none')
    