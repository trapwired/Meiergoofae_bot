import telepot
import random

class CocktailHandler(object):

    def __init__(self, config, bot : telepot.Bot):
        super().__init__()
        self.alkohol = config["alkohol"].replace("\n", "").split(",")
        self.alkoholmengen = list(map(int, config["alkoholmengen"].replace("\n", "").split(",")))
        self.mische = config["mische"].replace("\n", "").split(",")
        self.fancies = config["fancies"].replace("\n", "").split(",")
        self.extras = config["extras"].replace("\n", "").split(",")
        self.gifs = config["gifs"].replace("\n", "").split(",")
        self.personen = config["personen"].replace("\n", "").split(",")
        self.bot = bot

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