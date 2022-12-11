import fire
import os
from pygrambot.cli.templates import templates_list


class BotCli:
    def init(self):
        if not os.path.exists('config'):
            os.mkdir('config')
        for template in templates_list:
            with open(os.path.join('config/', template['name']), 'w+') as f:
                with open(template['path'], 'r') as sf:
                    f.write(sf.read())

    def start(self):
        from pygrambot.bot.bothandlers.bot import Bot
        Bot().start()


fire.Fire(BotCli)
