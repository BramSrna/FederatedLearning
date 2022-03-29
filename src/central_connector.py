class CentralConnector(object):
    def __init__(self):
        self.bot_list = []

    def add_bot(self, new_bot):
        for bot in self.bot_list:
            bot.add_new_bot(new_bot)
            new_bot.add_new_bot(bot)
        self.bot_list.append(new_bot)