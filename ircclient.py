#!/usr/bin/env python

# WS client example

import asyncio
import websockets

def setup():
    un = input("What username? ")
    return un

async def hello(un):
    while True:
        async with websockets.connect('ws://localhost:6789') as websocket:
            msg = input("message: ")
            print ("You said {m}".format(m=msg))
            packet = (un+" : "+msg)
            await websocket.send(packet)
            #msgs = await websocket.recv()
            #print(msgs)

asyncio.get_event_loop().run_until_complete(hello(setup()))
asyncio.get_event_loop().run_forever()
