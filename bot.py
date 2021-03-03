import discord
from discord.ext import commands
from types import FunctionType
import random
import os

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
from database import Database
from database_config import TABLES

# ---------------------------------------------------

intents = discord.Intents.all()
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
    """Reload a particular extension.\nUsage: `.cs reload (extension)`\nOnly Admins and Owners can use this!"""

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
    """Get help for a command or category.\nUsage: `.cs help <command> <category>`"""

    embed = discord.Embed(
        title="Help", description=f"Help for {command_help or 'Connection Server Bot'}"
    )

    embed.set_footer(text=f"Called by {ctx.author.display_name}.")
    embed.set_author(name=client.user.display_name)
    embed.set_thumbnail(url=client.user.avatar_url)

    cogs = client.cogs

    if command_help is None:

        for i in cogs.keys():
            embed.add_field(name=i + " cog", value=cogs[i].__doc__, inline=False)
        return await ctx.send(embed=embed)

    for i in cogs.keys():
        if i.lower() == command_help.lower():

            embed.add_field(name=i + " cog", value=cogs[i].__doc__, inline=False)

            commands = cogs[i].get_commands()

            for cmd in commands:
                embed.add_field(
                    name=".cs " + cmd.callback.__name__,
                    value=cmd.callback.__doc__,
                    inline=False,
                )

            return await ctx.send(embed=embed)

    cmds = [*client.commands]
    for i in cmds:
        if i.callback.__name__.lower() == command_help.lower():

            embed.add_field(
                name="Command: `.cs " + i.callback.__name__ + "`",
                value=i.callback.__doc__,
                inline=False,
            )

            return await ctx.send(embed=embed)

    await ctx.send(f"Command {command_help} not found!")


# ---------------------------------------------------


@client.listen("on_message")
async def on_msg(message):
    try: role_list = [i.name for i in message.author.roles]
    except: return 0
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
