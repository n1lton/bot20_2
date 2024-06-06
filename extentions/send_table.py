import discord
from discord.ext import commands
from assets import get_table
from models.Parameter import Parameter
from database import db


@commands.has_permissions(administrator=True)
@commands.command('создать-таблицу')
async def send_table(ctx: commands.Context):
    message = await ctx.send(
        get_table(),
        view=discord.ui.View(
            discord.Button(
                label='+ Внести данные',
                style=discord.ButtonStyle.primary,
                custom_id='add_data'
            )
        )
    )

    parameter = db.query(Parameter).filter(Parameter.name == 'message_id').first()
    if parameter:
        parameter.value = message.id

    else:
        db.add(Parameter())


def setup(bot: commands.Bot):
    bot.add_command(send_table)