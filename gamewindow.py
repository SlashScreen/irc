#gamewindow.py

import pygame
import asyncio
import websockets
import json
##Homegrown
import eventhandler
import movementhandler

pygame.init()
done = False
worlddict = {}
playerdict = {}
playerdict["name"] = input("Player Name? ")
screen = pygame.display.set_mode((400, 300))
playerdict["pos"] = {}
playerdict["pos"]["x"] = 0
playerdict["pos"]["y"] = 0
clock = pygame.time.Clock()
with open('config.json') as f:
    config = json.load(f)

def updateSelf(newWorld):
  print("do this later")

###MAIN LOOP###
async def mainLoop():
    global playerdict
    global movement
    global data
    global worlddict
    speed = 5
    square = 60
    direction = [0,0]
    tempdict = playerdict.copy()
    myfont = pygame.font.SysFont("monospace", 15)
    done = False
    while not done:
            async with websockets.connect('ws://'+config["server"]+':'+str(config["port"])) as websocket:
              event = eventhandler.constructEvent("p-update",playerdict)
              await websocket.send(event)
              dat = await websocket.recv()
              worlddict.update(eventhandler.handleEvent(dat,worlddict))
            w, h = pygame.display.get_surface().get_size()
            #control
            direction = movementhandler.calcInputEvent(pygame.event.get(),direction)
            #move player
            if direction == True:
              done = True
            else:
              playerdict["pos"]["x"] = playerdict["pos"]["x"] + (direction[0]*speed) 
              playerdict["pos"]["y"] = playerdict["pos"]["y"] + (direction[1]*speed)
            #clear cache or whatever
            pygame.display.flip()
            screen.fill((255, 255, 255))
            #get world

            if  not worlddict == {}:
              for name,player in worlddict["players"].items():
                  if not name == playerdict["name"]:
                      pygame.draw.rect(screen, (255, 128, 0), pygame.Rect(player["pos"]["x"], player["pos"]["y"], square, square))
                      label = myfont.render(name, 1, (0,0,0))
                      screen.blit(label, (player["pos"]["x"], player["pos"]["y"]))
            #draw client player
            pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(playerdict["pos"]["x"],playerdict["pos"]["y"], square, square)) #player
            clock.tick(60)

###INITIALIZE###
asyncio.get_event_loop().run_until_complete(mainLoop())
