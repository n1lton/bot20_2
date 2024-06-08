import discord
from database import db
from models.Region import Region
from models.Storage import Storage
from models.Parameter import Parameter
from bot import bot


def get_table():
    regions = db.query(Region).all()

    if not regions:
        return 'Склады отсутствуют'

    text = ''
    for region in regions:
        text += f'`{region.name.ljust(35)}`\n'

        for city in region.cities:
            text += f'**{city.name}**\n'

            for storage in city.storages:
                text += f'`{storage.name}` - `{storage.password}` - <t:{storage.expires}:R>\n'

        text += '\n'

    return text


async def update_message():
    message_id = db.query(Parameter).filter(Parameter.name == 'message_id').first().value
    channel_id = db.query(Parameter).filter(Parameter.name == 'channel_id').first().value
    channel = bot.get_channel(channel_id)
    message = await channel.fetch_message(message_id)
    await message.edit(content=get_table())