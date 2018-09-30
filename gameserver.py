#gameserver.py

import asyncio
import json
import websockets
##Homegrown
import eventhandler

messages = []
newlist = [1,2,3]
world = {}
world['players'] = {}
world['world'] = {}
world['world']['items'] = {}
clients = set()
with open('config.json') as f:
    config = json.load(f)

async def initialize(websocket):
    global world
    print("sent init to "+str(websocket))
    

async def gameServer(websocket,path):
    global world
    change = {}
    if not websocket in clients:
        websocket.send(eventhandler.constructEvent("init_world",world))
        #print("new client connected: {c}".format(c = str(websocket)))
        clients.add(websocket)
    tempworld = world.copy()
    msg = await websocket.recv()
    change.update(eventhandler.handleEvent(msg,world))
    world.update(change)
    f = open("./data/"+config["world"]+".json","w")
    json.dump(world,f)
    f.close()
    print(change)
    await websocket.send(eventhandler.constructEvent("w-update",change))
    messages.append(msg)

def getMsgs():
    return messages

def comeOnline():
    print ("Coming Online...")
    try:
        f = open("./data/"+config["world"]+".json","r+")
        world = json.load(f)
        f.close()
        print(str(world))
    except:
        print("json world file corrupt. Unable to load.")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    #start_server = websockets.serve(initialize, config["server"], config["port"])
    server = websockets.serve(gameServer, config["server"], config["port"])
    loop.run_until_complete(server)
    print ("Online!")
    loop.run_forever()

if __name__ == '__main__':
    comeOnline()
