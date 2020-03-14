import schedule
import time
import telepot
import quickstart as qs

class SchedulerHandler(object):

    def __init__(self, config, bot: telepot.Bot):
        super().__init__()
        self.bot = bot
        schedule.every().day.at("18:00").do(self.send_next_events)
        # schedule.every(20).seconds.do(self.send_next_events)
        
    def send_next_events(self):
        # TODO change chat_id to group chat id
        response = qs.getCalendarEntries()
        if len(response) > 0:
            self.bot.sendMessage(206738790, response)

    def run_schedule(self):
        schedule.run_pending()
 
    def handle(self, msg):
        pass
