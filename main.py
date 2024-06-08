import discord, config, os
from discord.ext import commands
from bot import bot

for i in os.listdir('extentions'):
    if i.endswith('.py'):
        bot.load_extension(f'extentions.{i.removesuffix(".py")}')

for i in os.listdir('events'):
    if i.endswith('.py'):
        bot.load_extension(f'events.{i.removesuffix(".py")}')

bot.run(config.TOKEN)
