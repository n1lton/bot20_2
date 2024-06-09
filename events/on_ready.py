import asyncio
from discord.ext import commands
from cache import cache
from database import db
from models.Storage import Storage
from assets import update_storage_state

async def on_ready():
    print('Bot is running.')
    for v in cache.values():
        v.cancel()

    cache.clear()

    for storage in db.query(Storage).all():
        cache[storage.id] = asyncio.create_task(update_storage_state(storage))


def setup(bot: commands.Bot):
    bot.event(on_ready)