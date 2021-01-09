import discord
from discord.ext import commands
import os

def get_token():
	with open("token.txt", "r") as f:
		token = f.read().strip()
	return token

token = get_token()

client = commands.Bot(command_prefix = ".cs ")

@client.listen('on_ready')
async def pr():
	print("Ready!")

@client.command()
async def reload(ctx, *extension):
	failed = []
	passed = []
	for i in extension:
		try:
			client.reload_extension(f"cogs.{i}")
			passed.append(i)
		except:
			failed.append(i)
	if passed != []: await ctx.send(f"Reloaded the extensions `{passed}` succesfully!")
	if failed != []: await ctx.send(f"Unable to load extensions: `{failed}`")


@client.listen('on_message')
async def process_msg(message):
	if message.mention_everyone and ("EveryonePing" not in [a.name for a in message.author.roles]):
		channel = message.channel
		author = message.author
		await message.delete()
		await channel.send(f"{author.mention}, please **do not** mention `@everyone or @here`")

for filename in os.listdir('./cogs'):
	if filename.endswith(".py"):
		print(f"cogs.{filename[:-3]}")
		client.load_extension(f"cogs.{filename[:-3]}")

client.run(token)