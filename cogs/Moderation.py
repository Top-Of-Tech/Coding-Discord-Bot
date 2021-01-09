import discord
from discord.ext import commands
import random
import datetime

class Moderation(commands.Cog):
	def __init__(self, client):
		self.client = client


	# Ban a User
	@commands.command()
	@commands.has_any_role('Admin', 'Owner')
	async def ban(self, ctx, member: discord.Member, reason):
		try:
			await ctx.guild.ban(member, reason=reason)
			await ctx.send(f"Succesfully banned {member}")
			print(f"Banned {member}")
		except Exception as e:
			await ctx.send(f"Was not able to ban `{member}`")
			await ctx.send(f"Error:\n```{e}```")


	# Purge Messages
	@commands.command()
	@commands.has_any_role('Admin', 'Owner')
	async def purge(self, ctx, limit=50, member: discord.Member=None):
		await ctx.message.delete()
		msg = []

		try:
			limit = int(limit)
		except:
			return await ctx.send("Please pass in an integer as limit")

		if not member:
			await ctx.channel.purge(limit=limit)
			return await ctx.send(f"Purged {limit} messages", delete_after=3)
		async for m in ctx.channel.history():
			if len(msg) == limit:
				break
			if m.author == member:
				msg.append(m)

		await ctx.channel.delete_messages(msg)
		await ctx.send(f"Purged {limit} messages of {member.mention}", delete_after=3)


	# Kick a user
	@commands.command()
	@commands.has_any_role('Admin', 'Owner')
	async def kick(self, ctx, member: discord.Member, *, reason=None):
		try:
			await member.kick(reason=reason)
			await ctx.send(f'User {member.mention} has kicked.')
		except Exception as e:
			await ctx.send(f"Was not able to kick `{member}`")
			await ctx.send(f"Error:\n```{e}```")


	# List the Modlogs of a user
	@commands.command()
	@commands.has_any_role('Admin', 'Owner')
	async def listlogs(self, ctx, member_id):
		
		logs = self.client.db.select(
			table = "ModLogs",
			columns = "ID, UserID, ModeratorID, Reason, Date",
			condition = f"UserID = {member_id}"
			)

		member = await self.client.fetch_user(member_id)
		
		embedVar = discord.Embed(title = f"Modlogs of {member.name}", description = f"{len(logs)} Modlogs", color = random_colour())
		
		for n, log in enumerate(logs):
			mod = await self.client.fetch_user(log[2])
			us = await self.client.fetch_user(log[1])
			m = f"ID: {log[0]}\n"
			m += f"User: {us.name}\n"
			m += f"Moderator: {mod.name}\n"
			m += f"Date: {log[4]}\n"
			
			embedVar.add_field(name = f"{n + 1}. {log[3]}", value = m, inline = False)
		
		await ctx.send(embed = embedVar)


	# Report a user
	@commands.command()
	async def report(self, ctx, member: discord.Member, *reason):
		reason = " ".join(reason).strip()
		n = len(self.client.db.select(table = "Reports", columns = "ID", condition = "ID > 0"))
		t = datetime.datetime.utcnow()
		form = t.strftime("%H:%M-%d-%m-%y")
		self.client.db.insert(table = "Reports", values = (n + 1, ctx.author.id, member.id, reason, form,0))
		await ctx.send(f"Reported {member.display_name} for {reason}.")


	# List reports
	@commands.command()
	async def listreports(self, ctx, resolved = 0, size = 5):

		logs = self.client.db.select(
			table = "Reports",
			columns = "ID, ReporterID, UserID, Reason, Date",
			size = size,
			condition = f"Resolved = {resolved}"
			)[:size]

		embedVar = discord.Embed(title = "Reports", description = f"{len(logs)} Reports", color = random_colour())
		
		for n, i in enumerate(logs):
			r = await self.client.fetch_user(i[1])
			m = f"ID: {i[0]}\n"
			m += f"Reporter: {r.name}\n"
			m += f"Reason: {i[3]}\n"
			m += f"Date: {i[4]}\n"
			u = await self.client.fetch_user(i[2])
			embedVar.add_field(name = f"{n + 1}. {u.name}", value = m, inline = False)
		
		await ctx.send(embed = embedVar)

	@commands.Cog.listener()
	async def on_message_edit(self, before, after):
		if before.author.id != self.client.user.id:
			embed = discord.Embed(title = "Edited Message", description = before.channel.mention, color = random_colour())
			embed.add_field(name = "Before", value = f"```{before.content}```", inline = True)
			embed.add_field(name = "After", value = f"```{after.content}```", inline = True)
			text = f"Time: {before.created_at}\nEdited at: {before.edited_at}\nMessage URL: {before.jump_url}\nMessage ID: {before.id}"
			embed.add_field(name = "Info", value = text, inline = False)
			await self.client.staff_channel.send(embed = embed)


	@commands.Cog.listener()
	async def on_message_delete(self, before):
		if before.author.id != self.client.user.id:
			embed = discord.Embed(title = "Deleted Message", description = before.channel.mention, color = random_colour())
			embed.add_field(name = "Message", value = f"```{before.content}```", inline = True)
			text = f"Time: {before.created_at}\nMessage ID: {before.id}"
			embed.add_field(name = "Info", value = text, inline = False)
			await self.client.staff_channel.send(embed = embed)


def random_colour():
	return discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def setup(client):
	client.add_cog(Moderation(client))