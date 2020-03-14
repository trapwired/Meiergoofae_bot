import random

class CocktailHandler(object):

    def __init__(self, config, bot):
        super().__init__()
        self.alkohol = config["alkohol"].split(",")
        self.alkoholmengen = list(map(int, config["alkoholmengen"].split(",")))
        self.mische = config["mische"].split(",")
        self.fancies = config["fancies"].split(",")
        self.extras = config["extras"].split(",")
        self.gifs = config["gifs"].split(",")
        self.personen = config["personen"].split(",")
        self.bot = bot

    def handle(self, msg):
        pass
