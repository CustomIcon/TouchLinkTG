from pyrogram import Client, filters, types, emoji
from tinydb import Query
from touchlink import database, utils



@Client.on_callback_query(filters.regex('^set_*'))
async def _(_, query):
    User = Query()
    data = query.data.split('_')
    if data[1] == "card":
        await query.message.edit_text("__Processing__")
        question = await query.from_user.ask("Send me the card number (located on top right corner of the card)", reply_markup=types.ForceReply())
        data = await utils.card.get_card_balance(question.text.replace(')', '').replace('(', ''))
        if data.success:
            database.update({'card': data.data.CardCan}, User.user_id == query.from_user.id)
            await query.message.reply(f"{emoji.CREDIT_CARD} Your card has been set to {data.data.CardCan}", reply_markup=types.InlineKeyboardMarkup([[types.InlineKeyboardButton('Back', callback_data='get_started')]]))