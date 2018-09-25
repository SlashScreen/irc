#gameserver.py

import asyncio
import json
import logging
import websockets
import ast
import eventhandler

logging.basicConfig()

messages = []
newlist = [1,2,3]
world = {}
world['players'] = {}
world['world'] = {}
world['world']['items'] = {}
with open('config.json') as f:
    config = json.load(f)

async def dictupdate(websocket,path):
    global world
    msg = await websocket.recv()
    world = eventhandler.handleEvent(msg,world)
    f = open("./data/"+config["world"]+".json","w")
    json.dump(world,f)
    f.close()
    
    await websocket.send(eventhandler.constructEvent("w-update",world))
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
    start_server = websockets.serve(dictupdate, config["server"], config["port"])
    loop.run_until_complete(start_server)
    print ("Online!")
    loop.run_forever()

if __name__ == '__main__':
    comeOnline()
