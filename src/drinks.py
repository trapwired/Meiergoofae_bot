import telepot
import random

class CocktailHandler(object):

    def __init__(self, config, bot : telepot.Bot):
        super().__init__()
        self.alkohol = self.clean_config(config["alkohol"])
        self.alkoholmengen = self.clean_config(config["alkoholmengen"])
        self.mische = self.clean_config(config["mische"])
        self.fancies = self.clean_config(config["fancies"])
        self.extras = self.clean_config(config["extras"])
        self.gifs = self.clean_config(config["gifs"])
        self.personen = self.clean_config(config["personen"])
        self.bot = bot

    @staticmethod
    def clean_config(raw_str):
        raw_list = raw_str.replace("\n", "").split(",")
        return list(map(lambda x: x.strip(), raw_list))

    def handle(self, msg):
        chat_id = msg['chat']['id']

        alkoholmenge = random.choice(self.alkoholmengen)
        alkohol = random.choice(self.alkohol)
        mische = random.choice(self.mische)
        person = random.choice(self.personen)
        fancy = random.choice(self.fancies)
        basename = mische if random.random() > 0.5 else alkohol
        namestr = f"{person}'s {basename} {fancy}"

        text = f"*{namestr}*\n"
        if random.random() > 0.2:
            text += f"\- Eis\n"
        text += f"\- {alkoholmenge}cl {alkohol}\n"
        text += f"\- {random.choice(self.extras)}\n"
        text += f"\- Auffüllen mit {mische}\n"

        self.bot.sendMessage(chat_id, text, parse_mode="MarkdownV2")
        self.bot.sendVideo(chat_id, random.choice(self.gifs))