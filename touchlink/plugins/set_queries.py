from pyrogram import Client, filters, types
from tinydb import Query
from touchlink import database, utils, loc



@Client.on_callback_query(filters.regex('^set_*'))
async def _(_, query):
    User = Query()
    data = query.data.split('_')
    user = database.search(User.user_id == query.from_user.id)
    if data[1] == "card":
        await query.message.delete()
        question = await query.from_user.ask(loc('send_card', user[0]['locale']), reply_markup=types.ForceReply())
        data = await utils.card.get_card_balance(question.text.replace(')', '').replace('(', ''))
        if data.success:
            database.update({'card': data.data.CardCan}, User.user_id == query.from_user.id)
            return await query.message.reply(loc('card_has_set', user[0]['locale']) + data.data.CardCan, reply_markup=types.InlineKeyboardMarkup([[types.InlineKeyboardButton('Back', callback_data='get_started')]]))
        return await query.message.reply(f"{data.message}", reply_markup=types.InlineKeyboardMarkup([[types.InlineKeyboardButton('Back', callback_data='get_started')]]))
    elif data[1] == "language":
        locale = user[0]['locale']
        database.update({'locale': 'div_MV' if locale == 'en_US' else 'en_US'}, User.user_id == query.from_user.id)
        await  query.message.delete()
        return await query.message.reply(
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