help_descriptions = \
{
    "General": {
        "Description": "Commands: `.cs help` and `.cs reload`",
        "help": "Get help for a command or category.\nUsage: `.cs help <command> <category>`",
        "reload": "Reload a particular extension.\nUsage: `.cs reload (extension)`\nOnly Admins and Owners can use this!"
    },
    "Moderation": {
        "Description": "Commands: `.cs purge`, `.cs ban`. `.cs kick`, `.cs listlogs`, `.cs report` and `.cs listreports`",
        "purge": "Purge the messages in a channel.\nUsage: `.cs purge <message_count> <user>`\nOnly Admins and Owners can use this!",
        "ban": "Ban a user.\nUsage: `.cs ban (user)`\nOnly Admins and Owners can use this!",
        "report": "Report a user.\nUsage: `.cs report (member) (reason)`",
        "listlogs": "List the logs of a user.\n Usage: `.cs listlogs (user id)`\nOnly Admins and Owners can use this!",
        "listreports": "List the reports created either resolved(1) or not resolved(0).\nUsage: `.cslistreports <resolved> <size>`"
    },
    "Admin": {
        "Description": "Commands: `.cs loadMembers`",
        "loadMembers": "Update the database to include the latest members (Hope to change this soon!).\nUsage: `.cs loadMembers`\nOnly Owners can use this!"
    }
}
# Do NOT modify this:
complete_dict = {}
for i in help_descriptions.keys():
    for j in help_descriptions[i].keys():
        if j != "Description":
            complete_dict[j.lower()] = help_descriptions[i][j]