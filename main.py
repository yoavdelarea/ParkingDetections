import threading

from app.VideoFeed import VideoFeed


if "__main__":
    v = VideoFeed()

    t1 = threading.Thread(target=v.run)

    t1.start()

    t1.join()
