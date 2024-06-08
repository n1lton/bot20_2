import discord, config
from discord.ext import commands
from models.Storage import Storage
from autocomplete import get_regions, get_cities_by_region, get_storages_by_region
from database import db
from modals import EditStorage, EditCity, EditRegion


@commands.slash_command(name='изменить', description='Изменить параметры региона, города или склада')
@discord.option('регион', str, required=True, autocomplete=get_regions,
    description='Имя региона', parameter_name='region_id')
@discord.option('город', str, required=False, autocomplete=get_cities_by_region,
    description='Имя города', parameter_name='city_id')
@discord.option('склад', str, required=False, autocomplete=get_storages_by_region,
    description='Имя склада', parameter_name='storage_id')
async def edit(ctx: discord.ApplicationContext, region_id, city_id, storage_id):
    if storage_id:
        await ctx.send_modal(EditStorage(storage_id))
    elif city_id:
        await ctx.send_modal(EditCity(city_id))
    else:
        await ctx.send_modal(EditRegion(region_id))


def setup(bot: commands.Bot):
    bot.add_application_command(edit)