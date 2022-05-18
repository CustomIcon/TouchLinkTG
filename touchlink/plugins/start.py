from pyrogram import Client, filters, types, emoji
from tinydb import Query
from touchlink import database, loc


@Client.on_message(filters.command('start'))
async def start(_, message):
    User = Query()
    if database.search(User.user_id == message.from_user.id):
        user = database.search(User.user_id == message.from_user.id)
        return await message.reply(
            loc('get_started', user[0]['locale']),
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
    else:
        # dont localize
        return await message.reply(
            "Hi there,\n"
            "I can help you manage your touchlink Bus cards from MTCC",
            reply_markup=types.InlineKeyboardMarkup(
                [[types.InlineKeyboardButton('Get started', callback_data='get_started')]]
            )
        )