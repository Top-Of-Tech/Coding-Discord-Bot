help_descriptions = \
{
    "General": {
        "Description": "Commands: `.cs help` and `.cs reload`",
        "help": "Get help for a command or category.\nUsage: `.cs help <command> <category>`",
        "reload": "Reload a particular extension.\nUsage: `.cs reload (extension)`\nOnly Admins and Owners can use this!"
    },
    "Moderation": {
        "Description": "Commands: `.cs purge`, `.cs ban`. `.cs kick`,`.cs closereport`, `.cs listlogs`, `.cs report` and `.cs listreports`",
        "purge": "Purge the messages in a channel.\nUsage: `.cs purge <message_count> <user>`\nOnly Admins and Owners can use this!",
        "ban": "Ban a user.\nUsage: `.cs ban (user)`\nOnly Admins and Owners can use this!",
        "report": "Report a user.\nUsage: `.cs report (member) (reason)`",
        "listlogs": "List the Modlogs of a user.\n Usage:\n`.cs listlogs (user id)` or `.cs ll (user id)`\nOnly Admins and Owners can use this!",
        "listreports": "List the reports created either resolved(1) or not resolved(0).\nUsage:\n`.cs listreports <resolved> <size>` or `.cs lr <resolved> <size>`",
        "closereport": "Close a report. \nUsage:\n`.cs closereport (report id)` or `.cs cr (report id)`\nCan only be used by Admins and Owners!"
    },
    "Admin": {
        "Description": "Commands: `.cs loadMembers`",
        "loadMembers": "Update the database to include the latest members that may have joined when the bot was down.\nUsage:\n`.cs loadMembers` or `.cs lm`\nOnly Owners can use this!"
    }
}
# Do NOT modify this:
complete_dict = {}
for i in help_descriptions.keys():
    for j in help_descriptions[i].keys():
        if j != "Description":
            complete_dict[j.lower()] = help_descriptions[i][j]