from subprocess import call
from pyrogram import Client, filters, types
from touchlink import database, loc
from tinydb import Query
from pyrogram import emoji
from aiohttp import ClientSession
from attrify import Attrify
from touchlink import utils


@Client.on_callback_query(filters.regex('^get_*'))
async def _(_, query):
    User = Query()
    data = query.data.split('_')
    if data[1] == 'started':
        if not database.search(User.user_id == query.from_user.id):
            database.insert({'user_id': query.from_user.id, 'locale': 'en_US', 'card': "0", 'banned': False})
        user = database.search(User.user_id == query.from_user.id)
        return await query.message.edit_text(loc('get_started', user[0]['locale']),
            reply_markup=types.InlineKeyboardMarkup(
                [
                    [types.InlineKeyboardButton(loc('get_balance', user[0]['locale']), callback_data='get_balance')],
                    [types.InlineKeyboardButton(loc('get_agency', user[0]['locale']), callback_data='get_agency')],
                    [types.InlineKeyboardButton(loc('get_stop', user[0]['locale']), callback_data='get_stop')],
                    [types.InlineKeyboardButton(
                        loc('set_language', user[0]['locale']),
                        callback_data='set_language'
                    )],
                ]
            )
        )
    elif data[1] == 'balance':
        user = database.search(User.user_id == query.from_user.id)
        if database.search(User.card == "0"):
            return await query.message.edit_text(
                loc('no_card', user[0]['locale']),
                reply_markup=types.InlineKeyboardMarkup(
                    [
                        [types.InlineKeyboardButton(loc('set_card', user[0]['locale']), callback_data='set_card')],
                    ]
                )
            )
        data = await utils.get_card_balance(user[0]['card'])
        if data.success:
            return await query.answer(loc('check_balance', user[0]['locale']) + str(data.data.Balance), show_alert=True)
    elif data[1] == 'agency':
        user = database.search(User.user_id == query.from_user.id)
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
            return await query.message.edit_text(string, disable_web_page_preview=True, reply_markup=types.InlineKeyboardMarkup([[types.InlineKeyboardButton(loc('back', user[0]['locale']), callback_data='get_started')]]))
    elif data[1] == 'stop':
        user = database.search(User.user_id == query.from_user.id)
        buttons = []
        for stop in (await utils.get_stops()).data:
            try:
                buttons.append([types.InlineKeyboardButton(f"{stop.name} ({stop.zone})", callback_data=f'stop_{stop._id}')])
            except AttributeError:
                buttons.append([types.InlineKeyboardButton(f"{stop.name}", callback_data=f'stop_{stop._id}')])
        buttons.append([types.InlineKeyboardButton(loc('back', user[0]['locale']), callback_data='get_started')])
        return await query.message.edit_text(loc('get_stops', user[0]['locale']), reply_markup=types.InlineKeyboardMarkup(buttons))