from guizero import App, Text
import ircserver



app = App(title="IRC")
message = Text(app, text="Welcome to the IRC server screen!")
allmessages = Text(app)
app.display()

##while True:
 #   messages = ircserver.getMsgs()
 #   allmessages.value = messages
 

