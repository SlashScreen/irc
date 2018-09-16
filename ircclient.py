#!/usr/bin/env python

# WS client example

import asyncio
import websockets
exdict = {}
exdict["w"] = "whoop"
exdict["list"] = [1,2,3,4,5]

def setup():
    un = input("What username? ")
    return un

def setupMsgPacket(un,msg):
    lun = len(un)
    lmsg = len(msg)
    lunout = str(lun).zfill(2)
 #   lmsgout = str("0"*(4-len(str(msg)))+str(len(msg)))
    print (lunout,un,msg)
    packet =  lunout+un+msg
    return packet
    #todo: size limitations

async def hello(un):
    while True:
        async with websockets.connect('ws://localhost:6789') as websocket:
 #           msg = input("message: ")
 #           print ("You said {m}".format(m=msg))
 #           packet = setupMsgPacket(un,msg)
   #        await websocket.send(packet)
            await websocket.send(str(exdict))

def online():
    asyncio.get_event_loop().run_until_complete(hello("g"))#setup()))
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    online()
