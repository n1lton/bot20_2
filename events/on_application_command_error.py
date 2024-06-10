import discord
from discord.ext import commands


async def on_application_command_error(ctx: discord.ApplicationContext, error):
    if isinstance(error, commands.errors.MissingPermissions) or isinstance(error, commands.MissingRole):
        await ctx.respond('❌ Нет прав на выполнение команды', ephemeral=True)

    else:
        raise error
    

def setup(bot):
    bot.event(on_application_command_error)