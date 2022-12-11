from pygrambot.data_objects.objects import UpdateDt, FormDt
from config.bot_settings import RELATIVE_PATH_TO_MIDDLEWARES
import time
from pygrambot.bot.botcommands.api_commands import SendCommand
from config.bot_settings import TOKEN


class NewMiddleware:
    """
    Class for creating middleware.
    To do this, you need to inherit from this class and implement the run method.
    """
    _middlewares_list: list = []
    enable: bool = True

    @classmethod
    async def run(cls, updatedt: UpdateDt) -> UpdateDt:
        """
        Middleware startup method.

        :return: UpdateDt
        """
        return updatedt


class ThrottlingMiddleware(NewMiddleware):
    time = time.time()
    users = {}
    timeout: float = 1
    message: str = 'Too many messages.'

    @classmethod
    async def set_message(cls, message: str):
        cls.message = message
        return cls

    @classmethod
    async def run(cls, updatedt: UpdateDt) -> UpdateDt:
        try:
            if not updatedt.message.id in cls.users.keys():
                cls.users[updatedt.message.id] = [updatedt.message.message_id, time.time()]
            else:
                t1 = cls.users[updatedt.message.id][1]
                t2 = time.time()
                mtime = t2 - t1
                if mtime < cls.timeout:
                    await SendCommand(TOKEN).sendMessage(chat_id=updatedt.message.id, text=cls.message,
                                                         reply_to_message_id=cls.users[updatedt.message.id][0])
                cls.users[updatedt.message.id] = [updatedt.message.message_id, time.time()]
        except Exception as e:
            print(f'ThrottlingMiddleware error: {e}')

        return updatedt

    @classmethod
    def set_timeout_sec(cls, value: float):
        cls.timeout = value
        return cls


class CatchNextMessageMiddleware(NewMiddleware):
    """
    Middleware that catches a single message and sends it for processing.
    """
    enable = True
    messages = []
    handler = None

    @classmethod
    async def add_message(cls, message_id):
        cls.messages.append(message_id)

    @classmethod
    async def run(cls, updatedt: UpdateDt) -> UpdateDt:
        if updatedt.message.id in cls.messages:
            updatedt.data['catch_msg'] = []
            updatedt.data['catch_msg'].append(updatedt)
            await cls.handler(updatedt)
            cls.messages.remove(updatedt.message.id)
        return updatedt

    async def test(self):
        print('tetetetststststs')


class CatchMultipleMessageMiddleware(NewMiddleware):
    """
    The middleware collects all messages according to the settings and runs the installed handler.
    """
    stop_commands = []
    messages: list = []
    handler = None

    @classmethod
    async def run(cls, updatedt: UpdateDt) -> UpdateDt:
        for cmm in cls.messages:
            if cmm == updatedt.message.id:
                # stop
                if updatedt.message.text in cls.stop_commands:
                    cls.messages.remove(cmm)
                else:
                    await cls.handler(updatedt)
        return updatedt


class FormMiddleware(NewMiddleware):
    """
    Middleware with which you can create forms and write data to them.
    """
    fields = []
    users_id = []

    handler = None
    formatter = None

    messages = {}

    @classmethod
    async def run(cls, updatedt: UpdateDt) -> UpdateDt:
        if updatedt.message.id in cls.users_id:
            # Writing form data.
            if not updatedt.message.id in cls.messages:
                cls.messages[updatedt.message.id] = []
                cls.messages[updatedt.message.id].append(updatedt.message.text)
            else:
                cls.messages[updatedt.message.id].append(updatedt.message.text)

            # Displays the name of the current field.
            if len(cls.messages[updatedt.message.id]) != len(cls.fields):
                await SendCommand(TOKEN).sendMessage(updatedt.message.id, f'{cls.fields[len(cls.messages[updatedt.message.id])]}:')

            # Actions after completing the form.
            if updatedt.message.id in cls.messages:
                if len(cls.messages[updatedt.message.id]) == len(cls.fields):
                    await cls.formatter(updatedt, cls.messages[updatedt.message.id])
                    await cls.handler(updatedt)
                    cls.users_id.remove(updatedt.message.id)
                    cls.messages.pop(updatedt.message.id)
        return updatedt


def get_middlewares() -> list[NewMiddleware]:
    """
    Returns a list with all middlewares.
    """
    middl = []
    for path in RELATIVE_PATH_TO_MIDDLEWARES:
        p = path.replace('/', '.').replace('\\', '.')
        if p.endswith('.'):
            p = p[:len(p) - 1] + p[len(p):]
        module = __import__(p, fromlist=['middlewares'])
        middl_module = getattr(module, 'middlewares')

        for i in middl_module.middlewareslist:
            middl.append(i)

    # append static middlewares
    middl.append(CatchNextMessageMiddleware)
    middl.append(CatchMultipleMessageMiddleware)
    middl.append(FormMiddleware)

    return middl
