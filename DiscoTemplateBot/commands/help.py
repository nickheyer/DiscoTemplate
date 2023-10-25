from DiscoTemplateBot.base_command import Command
from DiscoTemplateBot.managers.ui_manager import ListCommands
from DiscoTemplateBot.registry import CommandRegistry

class HelpCommand(Command):

    def __init__(self) -> None:
        super().__init__()
        self.name = "help"
        self.permissions = ["user", "developer", "unregistered"]
        self.description = "Display all authorized commands."
        self.aliases = ["help"]

    async def execute(self, message, ctx):
        registry = CommandRegistry()
        all_commands = registry.all()
        commands = ListCommands(ctx, all_commands)
        embed = await commands.generate_embed()
        await message.reply(embed=embed)