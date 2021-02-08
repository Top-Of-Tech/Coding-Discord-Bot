import discord
from discord.ext import commands

import psycopg2 as psg

from bot_help import help_descriptions, complete_dict
from bot_config import (
    REPORTS_CHANNEL,
    LOGS_CHANNEL,
    TOKEN,
    USERNAME,
    HOST,
    PASSWORD,
    PORT,
    DATABASE_NAME,
)
from database_config import TABLES

import random
import os


class Database:
    def __init__(self, db, user, password, host, port):
        self.Database = psg.connect(
            database=db, user=user, password=password, host=host, port=port
        )

        self.cursor = self.Database.cursor()

    def select(self, table, columns, condition, size=None, order_by=None):
        if order_by is None:
            self.cursor.execute(f"SELECT {columns} FROM {table} WHERE {condition};")
        else:
            self.cursor.execute(
                f"SELECT {columns} FROM {table} WHERE {condition} ORDER BY {order_by};"
            )
        if size is None:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchmany(size)

    def update(self, table, command, condition):
        try:
            self.cursor.execute(f"UPDATE {table} SET {command} WHERE {condition};")
            e = 1
        except Exception as j:
            e = j
            self.cursor.execute("ROLLBACK;")

        self.Database.commit()
        return e

    def insert(self, table, values: tuple):
        try:
            self.cursor.execute(f"INSERT INTO {table} VALUES {values};")
            e = 1
        except Exception as j:
            e = j
            self.cursor.execute("ROLLBACK;")

        self.Database.commit()
        return e

    def delete(self, table, condition):
        try:
            self.cursor.execute(f"DELETE FROM {table} WHERE {condition};")
            e = 1
        except Exception as j:
            e = j
            self.cursor.execute("ROLLBACK;")

        self.Database.commit()
        return e

    def insert_ignore(self, table, values):
        try:
            self.cursor.execute(
                f"INSERT INTO {table} VALUES {values} ON CONFLICT DO NOTHING;"
            )
            e = 1
        except Exception as j:
            e = j
            self.cursor.execute("ROLLBACK;")

        self.Database.commit()
        return e


# ---------------------------------------------------

intents = discord.Intents.default()
intents.messages = True
intents.members = True
client = commands.Bot(
    command_prefix=".cs ", intents=intents, help_command=None, case_insensitive=True
)
client.db = Database(
    db=DATABASE_NAME, user=USERNAME, password=PASSWORD, host=HOST, port=PORT
)

# ---------------------------------------------------

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        print(f"cogs.{filename[:-3]}")
        client.load_extension(f"cogs.{filename[:-3]}")


def random_colour():
    return discord.Colour.from_rgb(
        random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    )


# ---------------------------------------------------


@client.listen()
async def on_ready():
    print("Ready!")
    client.logs_channel = await client.fetch_channel(LOGS_CHANNEL)
    client.reports_channel = await client.fetch_channel(REPORTS_CHANNEL)

    results = client.db.select(
        table="information_schema.tables",
        columns="table_name",
        condition="table_schema = 'public';",
    )
    db_list = [i[0].lower() for i in results]

    for i in TABLES.keys():
        print(i)
        if i.lower() not in db_list:
            res = client.db.cursor.execute(TABLES[i])
            client.db.Database.commit()
            print("Created table", i)

    await client.change_presence(
        activity=discord.Game(name="Use the prefix `.cs` | .cs help")
    )


# ---------------------------------------------------


@client.listen()
async def on_member_join(member):
    print(
        member.name,
        client.db.insert(table="Members", values=(member.id, member.name, 0)),
    )


# ---------------------------------------------------


@client.listen()
async def on_user_update(before, after):
    print(
        before.name,
        client.db.update(
            table="Members",
            command=f"Username = '{after.name}'",
            condition=f"UserID = {before.id}",
        ),
    )


# ---------------------------------------------------


@client.command()
@commands.has_any_role("Owner", "Admin")
async def reload(ctx, *extension):
    failed = []
    passed = []
    for i in extension:
        try:
            client.reload_extension(f"cogs.{i}")
            passed.append(i)
        except:
            failed.append(i)
    if passed:
        await ctx.send(f"Reloaded the extensions `{passed}` succesfully!")
    if failed:
        await ctx.send(f"Unable to load extensions: `{failed}`")


# ---------------------------------------------------


@client.command()
async def help(ctx, command_help=None):
    if command_help is None:
        embed = discord.Embed(
            title="Help", description="Help for categories", color=random_colour()
        )

        for num, key in enumerate(help_descriptions.keys()):
            embed.add_field(
                name=key, value=help_descriptions[key]["Description"], inline=False
            )

    else:
        command_help = command_help.lower().strip()
        embed = discord.Embed(
            title=f"Help: {command_help.capitalize()}",
            description="",
            colour=random_colour(),
        )

        if command_help.capitalize() in help_descriptions.keys():
            h = help_descriptions[command_help.capitalize()]
            for key in help_descriptions[command_help.capitalize()].keys():
                embed.add_field(name=key, value=h[key], inline=False)

        elif command_help in complete_dict.keys():
            embed.add_field(
                name=f".cs {command_help}",
                value=complete_dict[command_help],
                inline=False,
            )

        else:
            embed.add_field(
                name="Not Found", value="Command/Category not found!", inline=False
            )

    embed.set_footer(text=f"Called by {ctx.author.display_name}.")
    embed.set_author(name=client.user.display_name)
    embed.set_thumbnail(url=client.user.avatar_url)

    await ctx.send(embed=embed)


# ---------------------------------------------------


@client.listen("on_message")
async def on_msg(message):
    role_list = [i.name for i in message.author.roles]
    mentions_allowed = (
        "Admin" in role_list or "Moderator" in role_list or "Owner" in role_list
    )
    if message.mention_everyone and not message.author.bot and not mentions_allowed:
        channel = message.channel
        author = message.author
        await message.delete()
        await channel.send(
            f"{author.mention}, please **do not** mention `@everyone or @here`"
        )
    try:
        user_id = message.author.id
        count = client.db.select(
            table="Members", columns="MsgsSent", condition=f"UserID = {user_id}"
        )
        m_count = count[0][0] + 1

        c = client.db.update(
            table="Members",
            command=f"MsgsSent = {m_count}",
            condition=f"UserID = {user_id}",
        )
    except:
        pass


# ---------------------------------------------------

try:
    client.run(TOKEN)
except Exception as e:
    print(e)
    client.db.Database.close()
