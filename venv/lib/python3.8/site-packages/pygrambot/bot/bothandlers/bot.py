from pygrambot.bot.bothandlers.handlers import Receiver, MainHandler
from config.bot_settings import TOKEN
import asyncio
from pygrambot.bot.botcommands.commands import NewCommand, get_commands
from pygrambot.bot.botcommands.api_commands import SendCommand
from pygrambot.bot.config import ACCEPT_ALL_MSG_COMMANDS


class Bot:
    def __init__(self):
        self.token = TOKEN
        self._sendcommand = SendCommand(self.token)
        queue = asyncio.Queue()
        self.receiver = Receiver(self.token, queue)
        self.main_handler = MainHandler(self.token, queue, 2)

    async def _set_commands_list(self):
        """
        Sets generated commands for the bot.
        """
        for comm in await get_commands():
            if not comm.command in ACCEPT_ALL_MSG_COMMANDS:
                comm.set_command_list()

        commands_list = []
        for bot_command in NewCommand.get_command_list():
            commands_list.append({"command": bot_command.command, "description": bot_command.description})
        await self._sendcommand.setMyCommands(commands_list)

    async def _handlers(self):
        """
        Start of all handlers for the bot to work.
        """
        await self._set_commands_list()
        await self.receiver.start()
        await self.main_handler.start()

    async def stop(self):
        """
        Stop all handlers.
        """

        await self.receiver.stop()
        await self.main_handler.stop()

    def start(self):
        """
        Start bot.
        """
        loop = asyncio.get_event_loop()
        try:
            print('Bot has been started.')
            loop.create_task(self._handlers())
            loop.run_forever()
        except KeyboardInterrupt:
            loop.run_until_complete(self.stop())
            print('\nBot has been stopped.')
