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
    Thread(target = ircwindow.start).start()
    Thread(target = ircserver.comeOnline).start()

