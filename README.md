# Discord-Bot
The open-source discord bot for our community - Connection Software

## Contribution
To start contributing, make sure you've joined our server, and our GitHub organisation! For ideas to contribute, take a look at `ideas.md`! Or if you already have an idea for the bot, go ahead with it!

1. Fork this git repository and clone it to your local machine

2. Make sure you are on the master/main branch before continuing.

3. Create a channel for the bot to send Logging info. Copy the channel id an modify line 14 of `bot.py` accordingly

4. Open `token.txt` and replace all the text in there with your token

5. Create a database, and place it's file path in line 15 of `bot.py`. Add 3 tables to it - Members, Reports and Modlogs. Create columns in each table as follows:

### Members:
| Column Name | Data Type | Other Properties |
| :---------: | :-------- | ---------------: |
| UserID | INTEGER | NOT NULL, UNIQUE|
| Username | TEXT | NOT NULL |
| NumLogs | INTEGER | NOT NULL |
| MsgsSent | INTEGER | NOT NULL |

### ModLogs
| Column Name | Data Type | Other Properties |
| :---------: | :-------- | ---------------: |
| ID | INTEGER | NOT NULL, UNIQUE|
| UserID | INTEGER | NOT NULL |
| ModeratorID | INTEGER | NOT NULL |
| Reason | TEXT | NOT NULL |
| Date | TEXT | NOT NULL |

### Reports
| Column Name | Data Type | Other Properties |
| :---------: | :-------- | ---------------: |
| ID | INTEGER | NOT NULL, UNIQUE|
| ReporterID | INTEGER | NOT NULL |
| UserID | INTEGER | NOT NULL |
| Reason | TEXT | NOT NULL |
| Date | TEXT | NOT NULL |
| Resolved | INTEGER  | NOT NULL DEFAULT 0|

5. Create a few records in the database `./cogs/ConnectionServerdb.db`.

6. You can add cogs in the cogs folder, and the bot will automatically load them.

7. Once you finish all your changes to the bot, make sure you update the help commands in `bot_help.py`

8. Once you finish all your changes to the bot, make sure you add a few lines at the end of `updates.md` stating what changes you made. If you have created a new table for the bot in the database, make sure to add the structure in `updates.md` too!

9. Then push it to the **fork that you created** and then open an Pull Request. Please make sure to remove all sensitive information like the bot token, the log channel id, and all records in the database.

10. Please **do not** make changes to `/cogs/Admin.py`, `/cogs/Moderation.py` and `bot.py`, except for the setup. Any Pull Requests with changes to these files other than the above mentioned 9 instructions **will NOT be accepted**

11. Trying to change the bot in any way to **obtain data meant only for staff, or private data will result in a warn/kick/ban.**
