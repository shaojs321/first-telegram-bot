from dataclasses import dataclass


class Message:
    pass
    #date
    #text
    #message_id
    #id
    #is_bot
    #first_name
    #username
    #language_cod


class Chat:
    pass
    #id
    #first_name
    #username
    #type


class UpdateDt:
    """
    One message.
    """

    update_id: int = None
    message: Message = None
    chat: Chat = None
    data: dict = {}

    def new_message(self):
        self.message = Message()

    def new_chat(self):
        self.chat = Chat()


@dataclass
class BotCommandDt:
    command: str
    description: str