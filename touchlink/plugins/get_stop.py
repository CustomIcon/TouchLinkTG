from pyrogram import Client, filters, types
from tinydb import Query
from touchlink import database, utils, loc



@Client.on_callback_query(filters.regex('^stop_*'))
async def _(_, query):
    User = Query()
    data = query.data.split('_')
    user = database.search(User.user_id == query.from_user.id)
    for stop in (await utils.get_stops()).data:
        if stop._id == data[1]:
            await query.message.delete()
            try:
                return await query.message.reply_venue(
                    latitude=stop.latitude,
                    longitude=stop.longitude,
                    title=stop.name,
                    address=stop.zone,
                    foursquare_id=stop.code,
                    reply_markup=types.InlineKeyboardMarkup(
                        [[types.InlineKeyboardButton(loc('back', user[0]['locale']), callback_data='stop_back')]]
                    )
                )
            except AttributeError:
                return await query.message.reply_venue(
                    latitude=stop.latitude,
                    longitude=stop.longitude,
                    title=stop.name,
                    address=stop.name,
                    foursquare_id=stop.code,
                    reply_markup=types.InlineKeyboardMarkup(
                        [[types.InlineKeyboardButton(loc('back', user[0]['locale']), callback_data='stop_back')]]
                    )
                )
        elif data[1] == 'back':
            await query.message.delete()
            buttons = []
            for stop in (await utils.get_stops()).data:
                # lazy staffs
                try:
                    buttons.append([types.InlineKeyboardButton(f"{stop.name} ({stop.zone})", callback_data=f'stop_{stop._id}')])
                except AttributeError:
                    buttons.append([types.InlineKeyboardButton(f"{stop.name}", callback_data=f'stop_{stop._id}')])
            buttons.append([types.InlineKeyboardButton(loc('back', user[0]['locale']), callback_data='get_started')])
            return await query.message.reply(loc('get_stops', user[0]['locale']), reply_markup=types.InlineKeyboardMarkup(buttons))