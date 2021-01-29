# Contributing

## Setup
1. Fork this Github repo, and clone it into your machine.

2. Host a PostgreSQL database. You can use your computer to do this by downloading PostgreSQL, or a hosting service like Heroku, or AwardSpace.

3. Create a file names `bot_config.py`, and copy-paste everything from `bot_config_sample.py` in it. Then change all the values accordingly.

4. In your testing server, create two roles - `Admin` and `Owner`

5. If you want, you can create a few records in each table. Use the command `.cs loadMembers` to add all the members in the server. Use the commands `.cs createrole`, `.cs report` and `.cs warn` to create roles, reports and warns.

6. Congratulations! The setup is now done! You can move on to `Code Layout`!

## Guidelines for Contributing
1. When you write code in this repository, please avoid:
	* Making changes to `bot.py`, `/cogs/Admin.py`, `/cogs/Moderation.py`, `/cogs/Roles.py` and `bot_config_sample.py`
	* Writing sensitive info like bot tokens in any of the files, _other_ than `bot_config.py`.
	* Editing any of the Markdown files, except `updates.md`

2. When you finish writing your code, please remember to:
	* Write a few lines in `updates.md` stating what changes you made.
	* If you added new commands, write a help command in `bot_help.py`
	* If you created a new table, be sure to specify the SQL syntax in `database_config.py`!

3. Please remember that whatever commands you write, you **may** not access data from the tables `ModLogs` and `Reports`

4. Writing malicious code, or anything of the like will result in a ban.