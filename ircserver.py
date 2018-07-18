#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets

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
    lun = int(packet[0:pktunlen-1])
    #lmsg = int(packet[pktunlen-1:pktunlen+pktmsglen-1])
    print (lun)
    un = packet[pktunlen:pktunlen+lun-1]
    msg = packet [pktunlen+lun:]
    out = [un,msg]
    return out

async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
 #   await register(websocket)
    msg = await websocket.recv()
    packet = getPacketData(msg)
    print(msg,packet)
    messages.append(msg)
    #await websocket.send('\n'+msg)
 #   await unregister(websocket)

def getMsgs():
    return messages

print ("Online")
start_server = websockets.serve(counter, 'localhost', 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
