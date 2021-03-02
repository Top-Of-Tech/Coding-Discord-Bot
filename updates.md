# Updates for Discord Bot
 All updates must be structured as:
 ## <User> - <Date> - <Short Description>
 	1. Made changes to . . . .
 	2. Updated bot to . . . .
 	.
 	.
 	.
## class PythonAddict - 09/01/2021 - Built Foundations for Bot
1. Built the foundations for the bot by adding admin and moderator commands
2. Built a framework for users to contribute
3. Configured basics of the bot -> staff channel, logging info, etc.

## class PythonAddict - 10/01/2021 - Added Help Command
1. Added Help command
2. Created bot_help.py for contributors to add documentation for their commands

## class PythonAddict - 10/01/2021 - Added closeReport Command
1. Added a closeReport command
2. Added aliases for each command
3. Fixed bugs

## class PythonAddict - 12/01/2021 - Added getrole, createrole, and deleterole Command
1. Added createrole command to add language roles to the DB
2. Added deleterole command to delete language roles from the DB
3. Added getrole command to obtain language roles

## Top-Of-Tech - 24/01/2021 - Formatted Files
1. Formatted files to comply with PEP 8

## Top-Of-Tech - 25/01/2021 - Added User Cog
1. Added user command to give general information about the user
2. Added avatar command to give the user's avatar

## class PythonAddict - 29/01/2021 - Migrated from SQLite
1. Changed database to PostgreSQL
2. Added files: `bot_config.py`, `bot_config_sample.py`

## class PythonAddict - 5/02/2021 - Removed Modlogs Table
1. Removed the Modlogs table, from now on, we will be using Dyno's Modlog system
2. Removed the warn command, we will be using Dyno's warning system
3. Added a `requirements.txt` file
4. Added a new idea in `ideas.md`

## class PythonAddict - 7/02/2021 - Fixed SQL Bugs
1. Fixed a bug in the SQL statement
2. Added Discord status message for the bot
3. Made commands case insensitive

## class PythonAddict - 8/02/2021 - Added rollbacks
1. Added roll backs for sql statements
2. Formatted files with black

## Top-Of-Tech - 25/02/2021 - Added Github cog
1. Added command to fetch github repo

## class PythonAddict - 28/02/2021 - Modified help commands
1. Modified help commands to use docstrings
2. Formatted files with black
3. Moved createrole and deleterole to the Roles cog.

## Top-Of-Tech 02/03/2021 - Added more Github commands
1. Added Github User command
2. Added Github Organization command