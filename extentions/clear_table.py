import discord, config
from discord.ext import commands
from assets import clear_channel, get_channel
from database import db
from models.Region import Region
from cache import cache


@commands.has_role(config.CAN_USE_BOT_ROLE_ID)
@commands.slash_command(name='очистить', description='Очищает таблицу со складами')
async def clear_table(ctx: discord.ApplicationContext):
    await ctx.respond('Таблица очищена', ephemeral=True)

    # отмена изменений состояния
    for v in cache.values():
        v.cancel()

    cache.clear()

    await clear_channel()

    channel = get_channel()
    await channel.send(
        view=discord.ui.View(
            discord.ui.Button(
                label='+ Добавить',
                style=discord.ButtonStyle.primary,
                custom_id='add_data'
            )
        )
    )

    for region in db.query(Region).all():
        db.delete(region)
        
    db.commit()


def setup(bot: commands.Bot):
    bot.add_application_command(clear_table)