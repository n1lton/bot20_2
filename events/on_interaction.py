import discord, config, time
from discord.ext import commands
from bot import bot
from modals import AddData
from assets import get_storage_text, reset_storage_update
from database import db
from models.City import City
from models.Storage import Storage


async def on_interaction(interaction: discord.Interaction):
    if interaction.custom_id and interaction.custom_id in ['add_data', 'update_city', 'update_storage']:
        if interaction.custom_id == 'add_data':
            await interaction.response.send_modal(modal=AddData())

        elif interaction.custom_id == 'update_city':
            await interaction.response.defer()

            city = db.query(City).filter(City.message_id == interaction.message.id).first()
            db.query(Storage).filter(
                Storage.city_id == city.id
            ).update({'expires': int(time.time()) + config.DEFAULT_EXPIRES})

            for storage in city.storages:
                reset_storage_update(storage)
                message = await interaction.channel.fetch_message(storage.message_id)
                await message.edit(content=get_storage_text(storage))

            db.commit()
                


        elif interaction.custom_id == 'update_storage':
            await interaction.response.defer()
            storage = db.query(Storage).filter(Storage.message_id == interaction.message.id).first()
            storage.expires = int(time.time()) + config.DEFAULT_EXPIRES
            reset_storage_update(storage)
            await interaction.message.edit(content=get_storage_text(storage))
            db.commit()


    else:
        await commands.Bot.on_interaction(bot, interaction)


def setup(bot: commands.Bot):
    bot.on_interaction = on_interaction