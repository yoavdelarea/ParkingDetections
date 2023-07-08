import threading

from app.VideoFeed import VideoFeed
from app.TelegramBot import TelegramBot

if "__main__":
    v = VideoFeed()
    telegram = TelegramBot()

    t1 = threading.Thread(target=v.run)
    t2 = threading.Thread(target=telegram.run)

    t1.start(), t2.start()

    t1.join(), t2.join()

