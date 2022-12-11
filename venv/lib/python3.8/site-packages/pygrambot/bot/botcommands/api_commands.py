import aiohttp
from typing import Optional
from pygrambot.telegram.keyboards import ReplyMarkup
from typing import BinaryIO
from pygrambot.exceptions.main_exc import ApiCommandError
import json


class SendCommand:
    def __init__(self, token):
        self.token = token

    async def _build_url(self, command: str):
        return f'https://api.telegram.org/bot{self.token}/{command}'

    async def _send_command(self, url: str, params: dict) -> dict:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=params) as responce:
                    res = await responce.json()
        except Exception as e:
            raise e
        if not res['ok']:
            raise ApiCommandError('setMyCommands')
        else:
            return res

    async def getUpdates(self, timeout: int = 0, offset: Optional[int] = 0) -> dict:
        """
        Receiving updates (messages) of the bot.
        """
        url = await self._build_url('getUpdates')
        params = {}
        if offset:
            params['offset'] = offset
        if timeout:
            params['timeout'] = timeout
        return await self._send_command(url, params)

    async def sendMessage(self, chat_id: str | int, text: str, parse_mode: str = 'HTML',
                          reply_markup: ReplyMarkup = None, reply_to_message_id: str = None) -> dict:
        url = await self._build_url('sendMessage')
        params = {}
        params['chat_id'] = chat_id
        params['text'] = text
        params['parse_mode'] = parse_mode
        if reply_markup:
            params['reply_markup'] = json.dumps(reply_markup.to_dict())
        if reply_to_message_id:
            params['reply_to_message_id'] = reply_to_message_id
        return await self._send_command(url, params)

    async def setMyCommands(self, commands: list[dict]) -> dict:
        url = await self._build_url('setMyCommands')
        params = json.dumps(commands)
        p = {'commands': params}
        return await self._send_command(url, p)

    async def deleteMyCommands(self) -> dict:
        url = await self._build_url('deleteMyCommands')
        params = {}
        return await self._send_command(url, params)

    async def getMyCommands(self) -> dict:
        url = await self._build_url('getMyCommands')
        params = {}
        return await self._send_command(url, params)

    async def deleteMessage(self, chat_id: str | int, message_id: int) -> dict:
        url = await self._build_url('deleteMessage')
        params = {}
        params['chat_id'] = chat_id
        params['message_id'] = message_id
        return await self._send_command(url, params)

    async def sendPhoto(self, chat_id: str | int, photo: str | BinaryIO, caption: Optional[str] = None,
                        parse_mode: str = 'HTML', reply_markup: ReplyMarkup = None):
        url = await self._build_url('sendPhoto')
        params = {}
        params['chat_id'] = chat_id
        params['photo'] = photo
        if caption:
            params['caption'] = caption
        if reply_markup:
            params['reply_markup'] = json.dumps(reply_markup.to_dict())
        params['parse_mode'] = parse_mode
        return await self._send_command(url, params)
