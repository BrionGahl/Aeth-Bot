#!/usr/bin/python3

import discord
from discord.ext import commands
import requests
import json

DEFAULT_REGION = 'us'
DEFAULT_LOCALE = 'en'

RAIDER_IMG = "https://cdnassets.raider.io/images/brand/Icon_FullColor_Square.png"
RAIDER_API = "https://raider.io/api/v1/"

class Raider(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(aliases=["affix"])
	@commands.cooldown(1, 60, commands.cooldowns.BucketType.default)
	async def affixes(self, ctx, *args):
		region = DEFAULT_REGION
		if len(args) == 1:
			region = args[0]
		elif len(args) > 1:
			await ctx.send("Error: too many arguments")
		
		parameters = {
			"region": region,
			"locale": DEFAULT_LOCALE
		}
		response = requests.get(RAIDER_API + "mythic-plus/affixes", params=parameters)
		
		if response.status_code != 200:
			await ctx.send("Error: did you input an incorrect region or locale?")
			return
		
		affix_data = response.json()['affix_details']
		
		embed = discord.Embed(title="This Week's Affixes")
		embed.set_thumbnail(url=RAIDER_IMG)
		for affix in affix_data:
			embed.add_field(name=affix['name'], value=affix['description'], inline=False)
		
		await ctx.send(embed=embed)
		return
	
	@affixes.error
	async def affixes_error(self, ctx, error):
		if isinstance(error, commands.CommandError): #add more to catch more errors such as cooldown
			await ctx.send("Usage: $affix [REGION]")
		return
			
	@commands.command(aliases=["raiderscore", "raider"])
	@commands.cooldown(1, 60, commands.cooldowns.BucketType.default)
	async def score(self, ctx, region, realm, char_name):
		parameters = {
			"region": region,
			"realm": realm,
			"name": char_name,
			"fields": "mythic_plus_scores_by_season:current"
		}
		response = requests.get(RAIDER_API + "characters/profile", params=parameters)
		if response.status_code != 200:
			await ctx.send("Error: Something went wrong. Did you input the correct region, realm, or name?")
			return
		
		embed = discord.Embed(title="Raider IO Score")
		embed.set_thumbnail(url=RAIDER_IMG)
		embed.add_field(name=response.json()['name'], value=response.json()['race'], inline=False)
		embed.add_field(name=response.json()['class'], value=response.json()['active_spec_name'], inline=False)
		embed.add_field(name="Score", value=response.json()["mythic_plus_scores_by_season"][0]['scores']['all'], inline=False)
		await ctx.send(embed=embed)
		return
		
	@score.error
	async def score_error(self, ctx, error):
		if isinstance(error, commands.CommandError): #add more to catch more errors such as cooldown
			await ctx.send("Usage: $score [REGION] [REALM] [CHARACTER]")
		return
		
def setup(bot):
		bot.add_cog(Raider(bot))
