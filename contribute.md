# Contributing

## Setup
1. Fork this Github repo, and clone it into your machine. Then install the requirements with `pip install -r requirements.txt`. You may do this in an environment.

2. Host a PostgreSQL database. You can use your computer to do this by downloading PostgreSQL, or a hosting service like Heroku, or AwardSpace.

3. Create a file named `bot_config.py`, and copy-paste everything from `bot_config_sample.py` into it. Then change all the values accordingly.

4. In your testing server, create two roles - `Admin` and `Owner`

5. If you want, you can create a few records in each table. Use the command `.cs loadMembers` to add all the members in the server. Use the command `.cs createrole` to create roles.

6. Congratulations! The setup is now done! You can move on to [code_layout.md](./code_layout.md)!

## Guidelines for Contributing
1. When you write code in this repository, please avoid:
	* Making changes to `bot.py`, `/cogs/Admin.py`, `/cogs/Moderation.py`, and `bot_config_sample.py` _unless_ you spot a bug in them.
	* Writing sensitive info like bot tokens in any of the files, _other_ than `bot_config.py`.
	* Editing any of the Markdown files, except `updates.md`. However, you may do this if any of the information has become irrelevant.

2. When you finish writing your code, please remember to:
	* Write a few lines in [updates.md](./updates.md) stating what changes you made.
	* If you added new commands, write a help command in the form of a doc string for the cog and/or commands!
	* If you created a new table, be sure to specify the SQL syntax in `database_config.py`!

3. Writing malicious code, or anything of the like will result in a ban.
