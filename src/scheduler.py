import schedule
import time
import telepot
import quickstart as qs

class SchedulerHandler(object):

    def __init__(self, config, bot: telepot.Bot):
        super().__init__()
        self.bot = bot
        self.group_id = config['group_id']
        schedule.every().day.at("18:00").do(self.send_next_events)
        schedule.every().tuesday.at("14:00").do(self.send_ct)
        # schedule.every(20).seconds.do(self.send_next_events)
        
    def send_next_events(self):
        # TODO change chat_id to group chat id
        response = qs.getCalendarEntries()
        if len(response) > 0:
            self.bot.sendMessage(self.group_id, response)

    def send_ct(self):
        self.bot.sendMessage(self.group_id, 'It\'s cocktail tuesday, meiergööfler')
        
    def run_schedule(self):
        schedule.run_pending()
 
    def handle(self, msg):
        pass
