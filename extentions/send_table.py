import discord
from discord.ext import commands
from assets import get_table
from models.Parameter import Parameter
from database import db


@commands.has_permissions(administrator=True)
@commands.command('создать-таблицу')
async def send_table(ctx: commands.Context):
    message = await ctx.send(
        view=discord.ui.View(
            discord.ui.Button(
                label='+ Добавить',
                style=discord.ButtonStyle.primary,
                custom_id='add_data'
            )
        )
    )

    channel_parameter = db.query(Parameter).filter(Parameter.name == 'channel_id').first()
    if channel_parameter:
        channel_parameter.value = message.channel.id

    else:
        db.add(Parameter(name='channel_id', value=message.channel.id))

    db.commit()


def setup(bot: commands.Bot):
    bot.add_command(send_table)