import discord
from discord.ext import commands
import os
from sqlite3 import connect
import sqlite3
from bot_help import help_descriptions, complete_dict
import random

def get_token():
	with open("token.txt", "r") as f:
		token = f.read().strip()
	return token

token = get_token()
DB_PATH = "" # Path to DB
LOGS_CHANNEL = #Staff channel id as an integer


class database():
	def __init__(self, db):
		self.Database = connect(db)
		self.cursor = self.Database.cursor()

	def select(self, table, columns, condition, size = None, order_by = None):
		if order_by is None:
			self.cursor.execute(f"SELECT {columns} FROM {table} WHERE {condition};")
		else:
			self.cursor.execute(f"SELECT {columns} FROM {table} WHERE {condition} ORDER BY {order_by};")
		if size is None:
			return self.cursor.fetchall()
		else:
			return self.cursor.fetchmany(size)

	def update(self, table, command, condition):
		try:
			self.cursor.execute(f"UPDATE {table} SET {command} WHERE {condition};")
			self.Database.commit()
			return 1
		except sqlite3.Error as e:
			return e

	def insert(self, table, values: tuple):
		try:
			self.cursor.execute(f"INSERT INTO {table} VALUES {values};")
			self.Database.commit()
			return 1
		except sqlite3.Error as e:
			return e

	def delete(self, table, condition):
		try:
			self.cursor.execute(f"DELETE FROM {table} WHERE {condition};")
			self.Database.commit()
			return 1
		except sqlite3.Error as e:
			return e

# ---------------------------------------------------

intents = discord.Intents.default()
intents.messages = True
intents.members = True
client = commands.Bot(command_prefix = ".cs ", intents = intents, help_command = None)
client.db = database(DB_PATH)

# ---------------------------------------------------

for filename in os.listdir('./cogs'):
	if filename.endswith(".py"):
		print(f"cogs.{filename[:-3]}")
		client.load_extension(f"cogs.{filename[:-3]}")

def random_colour():
	return discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# ---------------------------------------------------

@client.listen()
async def on_ready():
	print("Ready!")
	client.logs_channel = await client.fetch_channel(LOGS_CHANNEL)

# ---------------------------------------------------

@client.listen()
async def on_member_join(member):
	print(member.name, client.db.insert(table = "Members", values = (member.id, member.name, 0, 0)))

# ---------------------------------------------------

@client.listen()
async def on_user_update(before, after):
	print(before.name, client.db.update(table = "Members", command = f"Username = '{after.name}'", condition = f"UserID = {before.id}"))

# ---------------------------------------------------

@client.command()
@commands.has_any_role('Owner', 'Admin')
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

# ---------------------------------------------------

@client.command()
async def help(ctx, commandHelp = None):
	if commandHelp is None:
		embed = discord.Embed(title = "Help", description = "Help for categories", color = random_colour())

		for num, key in enumerate(help_descriptions.keys()):
			embed.add_field(name = key, value = help_descriptions[key]["Description"], inline = False)

	else:
		command_help = commandHelp.lower().strip()
		embed = discord.Embed(title = f"Help: {command_help.capitalize()}", description = "", colour = random_colour())

		if command_help.capitalize() in help_descriptions.keys():
			h = help_descriptions[command_help.capitalize()]
			for key in help_descriptions[command_help.capitalize()].keys():
				embed.add_field(name = key, value = h[key], inline = False)

		elif command_help in complete_dict.keys():
			embed.add_field(name = f".cs {command_help}", value = complete_dict[command_help], inline = False)

		else:
			embed.add_field(name = "Not Found", value = "Command/Category not found!", inline = False)

	embed.set_footer(text=f"Called by {ctx.author.display_name}.")
	embed.set_author(name=client.user.display_name)
	embed.set_thumbnail(url=client.user.avatar_url)

	await ctx.send(embed=embed)

# ---------------------------------------------------

@client.listen('on_message')
async def process_msg(message):
	if message.mention_everyone and ("EveryonePing" not in [a.name for a in message.author.roles]):
		channel = message.channel
		author = message.author
		await message.delete()
		await channel.send(f"{author.mention}, please **do not** mention `@everyone or @here`")
	try:
		user_id = message.author.id
		count = client.db.select(table = "Members", columns = "MsgsSent", condition = f"UserID = {user_id}")
		m_count = count[0][0] + 1

		c = client.db.update(table = "Members", command = f"MsgsSent = {m_count}", condition = f"UserID = {user_id}")
	except:
		pass

# ---------------------------------------------------

try:
	client.run(token)
except:
	client.db.cursor.close()