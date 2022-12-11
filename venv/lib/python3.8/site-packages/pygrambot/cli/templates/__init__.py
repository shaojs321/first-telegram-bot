from pygrambot.cli.templates import bot_settings


templates_list = [
    {'name': 'bot_settings.py', 'path': bot_settings.__file__}
]

if __name__ == '__main__':
    print(bot_settings.__file__)