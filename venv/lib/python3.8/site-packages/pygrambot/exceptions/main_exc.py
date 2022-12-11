from .base import BotBaseException


class UpdateError(BotBaseException):
    def __init__(self):
        super().__init__('Error getting update. Status "ok": false.')


class ApiCommandError(BotBaseException):
    def __init__(self, command: str):
        super().__init__(f'Error sending command "{command}".')
