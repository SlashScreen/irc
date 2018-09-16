from appJar import gui
from tkinter import *

class Application(Frame):
    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


def startappjar():
    print("Window init")
    app = gui()
    text = app.addLabel("text")
    print("Window open")
    app.go()

def start():
    root = Tk()
    app = Application(master=root)
    app.mainloop()
    root.destroy()

if __name__ == '__main__':
    startappjar()
