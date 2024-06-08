import discord
from database import db
from models.Region import Region
from models.City import City
from models.Storage import Storage


def get_regions(ctx: discord.AutocompleteContext):
    regions = db.query(Region).all()
    return [
        discord.OptionChoice(name=region.name, value=str(region.id)) for region in regions \
        if region.name.lower().startswith(ctx.value.lower())
    ]


def get_cities_by_region(ctx: discord.AutocompleteContext):
    region_id = ctx.options['регион']
    cities = db.query(City).filter(City.region_id == region_id).all()
    return [
        discord.OptionChoice(name=city.name, value=str(city.id)) for city in cities \
        if city.name.lower().startswith(ctx.value.lower())
    ]

def get_storages_by_region(ctx: discord.AutocompleteContext):
    city_id = ctx.options['город']
    storages = db.query(Storage).filter(Storage.city_id == city_id).all()
    return [
        discord.OptionChoice(name=storage.name, value=str(storage.id)) for storage in storages \
        if storage.name.lower().startswith(ctx.value.lower())
    ]