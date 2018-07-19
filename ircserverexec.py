import threading
from threading import Thread
import ircwindow
import ircserver

def execute(func):
    if func == "win":
        ircwindow.start()
    else:
        ircserver.comeOnline()

#ircserver.comeOnline()

if __name__ == '__main__':
    win = Thread(target = ircwindow.start)
    server = Thread(target = ircserver.comeOnline)
    win.start()
    server.start()
    win.join()
    server.join()
