import discord, time, config
from discord.ext import commands
from models.Storage import Storage
from autocomplete import get_regions, get_cities_by_region, get_storages_by_region
from assets import update_message
from database import db


@commands.slash_command(name='обновить-таймер', description='Обновить таймер конкретного склада или по городу')
@discord.option('регион', str, required=True, autocomplete=get_regions,
    description='Имя региона', parameter_name='region_id')
@discord.option('город', str, required=True, autocomplete=get_cities_by_region,
    description='Имя города', parameter_name='city_id')
@discord.option('склад', str, required=False, autocomplete=get_storages_by_region,
    description='Имя склада', parameter_name='storage_id')
async def edit(ctx: discord.ApplicationContext, region_id, city_id, storage_id):
    if storage_id:
        storage = db.query(Storage).filter(Storage.id == storage_id).first()
        storage.expires = int(time.time()) + config.DEFAULT_EXPIRES

    else:
        db.query(Storage).filter(Storage.city_id == city_id).update(
            {'expires': int(time.time()) + config.DEFAULT_EXPIRES}
        )

    db.commit()
    await ctx.respond('✅ Таймер успешно обновлён', ephemeral=True)
    await update_message()


def setup(bot: commands.Bot):
    bot.add_application_command(edit)