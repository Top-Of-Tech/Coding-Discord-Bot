# Discord Bot for the Connection Server

## Database
The bot uses an PostgreSQL database to maintain records. As of now, it has three tables - Members, Modlogs, and Roles
Of these 3 tables, you can only obtain data from the Members and Roles tables. 

The database for the client is defined as `client.db`. To insert, update, delete or fetch records, use code like this:
```py

# INSERT INTO table VALUES(values);
client.db.insert(table = "Members", values = (100011100000, "UserName", 0, 0))

# UPDATE table SET command WHERE condition;
client.db.update(table = "Members", command = "MsgsSent = 100", condition = "UserID = 11111111111")

# DELETE FROM table WHERE condition;
client.db.delete(table = "Members", condition = "UserID = 1111111111")

# SELECT columns FROM table WHERE condition ORDER BY order_by;
members= self.client.db.select(table="Members", columns="*", condition=f"UserID = 11100011", order_by="MsgsSent")
```
Note that all parameters must be in SQL syntax

## Client

All commands for the client must be written in the form of cogs. Place all your cogs in the `./cogs` folder, and the bot will automatically load them.

Prefix for bot commands is `.cs `. For ideas on contributions that you can make, look at [ideas.md](./ideas.md)!

## Files

`bot.py` - File to run the bot
`bot_config.py` - Contains sensitive info to run the bot, and is listed in the .gitignore file (You dont need to erase it everytime you push!)
`database_config.py` - Contains SQL statements to create tables.