#!/usr/bin/python3

import logging
import discord
from discord.ext import commands
import loader

VERSION = '0.1'
DESCRIPTION = 'AETH-BOT\nAuthor: Brion Gahl\n'

bot = commands.Bot(command_prefix=loader.PREFIX, description=DESCRIPTION) 

@bot.event
async def on_ready():
	print("LOGGED IN AS {0.user}".format(bot))
	bot.load_extension('cogs.raider')

@bot.command(name="test")
async def _hello(ctx):
	await ctx.send("test")

if __name__ == '__main__':
	bot.run(loader.TOKEN)
