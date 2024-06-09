import discord, config
from discord.ext import commands
from models.Storage import Storage
from autocomplete import get_regions, get_cities_by_region, get_storages_by_region
from database import db
from modals import EditStorage, EditCity, EditRegion
from models.Region import Region
from models.City import City
from models.Storage import Storage


@commands.slash_command(name='изменить', description='Изменить параметры региона, города или склада')
@discord.option('регион', str, required=True, autocomplete=get_regions,
    description='Имя региона', parameter_name='region_id')
@discord.option('город', str, required=False, autocomplete=get_cities_by_region,
    description='Имя города', parameter_name='city_id')
@discord.option('склад', str, required=False, autocomplete=get_storages_by_region,
    description='Имя склада', parameter_name='storage_id')
async def edit(ctx: discord.ApplicationContext, region_id, city_id, storage_id):
    if storage_id:
        storage = db.query(Storage).filter(Storage.id == storage_id).first()
        if not storage:
            await ctx.respond('❌ Необходимо выбрать склад из списка', ephemeral=True)
            return
        await ctx.send_modal(EditStorage(storage_id))
    elif city_id:
        city = db.query(City).filter(City.id == city_id).first()
        if not city:
            await ctx.respond('❌ Необходимо выбрать город из списка', ephemeral=True)
            return
        await ctx.send_modal(EditCity(city_id))
    else:
        region = db.query(Region).filter(Region.id == region_id).first()
        if not region:
            await ctx.respond('❌ Необходимо выбрать регион из списка', ephemeral=True)
            return
        await ctx.send_modal(EditRegion(region_id))


def setup(bot: commands.Bot):
    bot.add_application_command(edit)