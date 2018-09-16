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

USERS = set()

def state_event():
    return json.dumps({'type': 'state', **STATE})

def users_event():
    return json.dumps({'type': 'users', 'count': len(USERS)})

async def notify_state():
    if USERS:       # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def notify_users():
    if USERS:       # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def register(websocket):
    USERS.add(websocket)
    await notify_users()

async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()

def getPacketData(packet):
    pktunlen = 2
    lun = int(packet[0:pktunlen])
    print (lun)
    un = packet[pktunlen:pktunlen+lun]
    msg = packet [pktunlen+lun:]
    out = {"username":un,"message":msg}
    return out

async def counter(websocket, path):
    msg = await websocket.recv()
    packet = getPacketData(msg)
    print("{u} said: {m}".format(u = packet["username"], m = packet["message"]))
    messages.append(msg)

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
    start_server = websockets.serve(dictupdate, 'localhost', 6789)
    loop.run_until_complete(start_server)
    print ("Online!")
    loop.run_forever()

if __name__ == '__main__':
 #   locdict = {}
    comeOnline()
