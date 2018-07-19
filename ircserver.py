#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets
import ircwindow

logging.basicConfig()

messages = []
newlist = [1,2,3]

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
    # register(websocket) sends user_event() to websocket
 #   await register(websocket)
    msg = await websocket.recv()
    packet = getPacketData(msg)
    print("{u} said: {m}".format(u = packet["username"], m = packet["message"]))
    messages.append(msg)
    #await websocket.send('\n'+msg)
 #   await unregister(websocket)

def getMsgs():
    return messages

def comeOnline():
    print ("Online")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_server = websockets.serve(counter, 'localhost', 6789)
    loop.run_until_complete(start_server)
    loop.run_forever()

if __name__ == '__main__':
    comeOnline()
