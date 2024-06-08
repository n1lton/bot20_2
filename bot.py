import discord, config
from discord.ext import commands

bot = commands.Bot(command_prefix=config.PREFIX, intents=discord.Intents.all(), debug_guilds=[1243251110844825621])