import discord
from discord.ext import commands
import os
from sqlite3 import connect
import sqlite3

def get_token():
	with open("token.txt", "r") as f:
		token = f.read().strip()
	return token

token = get_token()
DB_PATH = "" # Create a database and place its path here
LOGS_CHANNEL = "Your Logs Channel as an integer"


class database():
	def __init__(self, db = ".\\cogs\\ConnectionServerdb.db"):
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

	def insert(self, table, values: tuple, ignore = False):
		try:
			if ignore:
				self.cursor.execute(f"INSERT IGNORE INTO {table} VALUES {values};")
			else:
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

intents = discord.Intents.default()
intents.messages = True
client = commands.Bot(command_prefix = ".cs ", intents = intents)
client.db = database(DB_PATH)


for filename in os.listdir('./cogs'):
	if filename.endswith(".py"):
		print(f"cogs.{filename[:-3]}")
		client.load_extension(f"cogs.{filename[:-3]}")

@client.listen('on_ready')
async def pr():
	print("Ready!")
	client.staff_channel = await client.fetch_channel(STAFF_CHANNEL)

@client.command()
@commands.has_any_role(self.client.Owner_Role, self.client.Admin_Role)
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
	try:
		user_id = message.author.id
		count = client.db.select(table = "Members", columns = "MsgsSent", condition = f"UserID = {user_id}")
		m_count = count[0][0] + 1

		c = client.db.update(table = "Members", command = f"MsgsSent = {m_count}", condition = f"UserID = {user_id}")
	except:
		pass

try:
	client.run(token)
except:
	client.db.cursor.close()