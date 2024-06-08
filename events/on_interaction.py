import discord, config
from discord.ext import commands
from bot import bot
from modals import AddData


async def on_interaction(interaction: discord.Interaction):
    if interaction.custom_id and interaction.custom_id == 'add_data':
        await interaction.response.send_modal(modal=AddData())

    else:
        await commands.Bot.on_interaction(bot, interaction)


def setup(bot: commands.Bot):
    bot.on_interaction = on_interaction