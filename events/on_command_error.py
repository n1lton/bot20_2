import discord
from discord.ext import commands


async def on_command_error(ctx: commands.Context, error):
    if isinstance(error, commands.MissingPermissions) \
            or isinstance(error, commands.MissingRole) \
            or isinstance(error, commands.CommandNotFound):
        pass

    else:
        raise error
    

def setup(bot):
    bot.event(on_command_error)