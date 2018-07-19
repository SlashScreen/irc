from appJar import gui

def start():
    print("Window init")
    app = gui()
    text = app.addLabel("text")
    print("Window open")
    app.go()

if __name__ == '__main__':
    start()
