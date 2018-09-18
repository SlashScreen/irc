#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets
import ast

logging.basicConfig()

messages = []
newlist = [1,2,3]
world = {}
world['players'] = {}
with open('config.json') as f:
    data = json.load(f)

async def dictupdate(websocket,path):
    msg = await websocket.recv()
    raw = ast.literal_eval(msg)
    global world
    if not raw == world:
        world["players"][raw["name"]] = raw
        f = open("./data/testworld.txt","w")
        f.write(str(world))
        f.close()
        print(str(world))
        await websocket.send(str(world))
        messages.append(msg)

def getMsgs():
    return messages

def comeOnline():
    print ("Coming Online...")
    #try:
    f = open("./data/testworld.txt","r+")
    worldread = f.read()
    print(worldread)
    world = ast.literal_eval(worldread)
    f.close()
    #except:
    #print ("cannot read world file.")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_server = websockets.serve(dictupdate, data["server"], 12250)
    loop.run_until_complete(start_server)
    print ("Online!")
    loop.run_forever()

if __name__ == '__main__':
 #   locdict = {}
    comeOnline()
