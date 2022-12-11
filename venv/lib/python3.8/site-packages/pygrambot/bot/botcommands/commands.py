from typing import Callable, Type
from config.bot_settings import RELATIVE_PATH_TO_COMMANDS
import importlib
from pygrambot.data_objects.objects import BotCommandDt


class NewCommand:
    """
    To create a new team, you need to inherit from this class and fill in the fields.
    """
    _all_commands: list[BotCommandDt] = []

    # command "*" - receives all messages
    command: str = None
    description: str = None
    handler: Callable = None

    @classmethod
    def set_command_list(cls):
        """
        Adds a command (BotCommandDt) to the general list.
        """
        cls.command = str(cls.command)
        cls.description = str(cls.description)

        if not cls.command.startswith('/'):
            cls.command = '/' + cls.command
        cls._all_commands.append(BotCommandDt(command=cls.command, description=cls.description))

    @classmethod
    def get_command_list(cls) -> list[BotCommandDt]:
        return cls._all_commands


async def get_commands() -> list[Type[NewCommand]]:
    """
    Return all created commands.
    """
    commands = []
    for path in RELATIVE_PATH_TO_COMMANDS:
        p = path.replace('/', '.').replace('\\', '.')
        if p.endswith('.'):
            p = p[:len(p)-1] + p[len(p):]
        p += '.commands'
        importlib.import_module(p)
        for command in NewCommand.__subclasses__():
            commands.append(command)
    return commands
