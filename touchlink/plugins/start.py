from pyrogram import Client, filters, types, emoji
from tinydb import Query
from touchlink import database


@Client.on_message(filters.command('start'))
async def start(_, message):
    User = Query()
    if database.search(User.user_id == message.from_user.id):
        return await message.reply(
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
    else:
        return await message.reply(
            "Hi there,\n"
            "I can help you manage your touchlink Bus cards from MTCC",
            reply_markup=types.InlineKeyboardMarkup(
                [[types.InlineKeyboardButton('Get started', callback_data='get_started')]]
            )
        )