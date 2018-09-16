import pygame
import ircclient as client
from multiprocessing import Process
import asyncio
import websockets
import ast


pygame.init()
screen = pygame.display.set_mode((400, 300))
done = False
worlddict = {}
playerdict = {}
playerdict["name"] = input("Player Name? ")
playerdict["pos"] = {}
playerdict["pos"]["x"] = 0
playerdict["pos"]["y"] = 0
clock = pygame.time.Clock()

def runInParallel(*fns):
  proc = []
  for fn in fns:
    p = Process(target=fn)
    p.start()
    proc.append(p)
  for p in proc:
    p.join()

###MAIN LOOP###
async def mainLoop():
    global playerdict
    done = False
    while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                key = pygame.key.get_pressed()
                if key[pygame.K_d]:
                    playerdict["pos"]["x"] += 1
                if key[pygame.K_a]:
                    playerdict["pos"]["x"] -= 1
                if key[pygame.K_w]:
                    playerdict["pos"]["y"] -= 1
                if key[pygame.K_s]:
                    playerdict["pos"]["y"] += 1
            pygame.display.flip()
            screen.fill((255, 255, 255))
            pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(playerdict["pos"]["x"], playerdict["pos"]["y"], 60, 60))
            async with websockets.connect('ws://localhost:6789') as websocket:
                await websocket.send(str(playerdict))
                dat = await websocket.recv()
                raw =  ast.literal_eval(dat)
                #print(raw)
                for name,player in raw.items():
                    #print (player)
                    if not name == playerdict["name"]:
                        pygame.draw.rect(screen, (255, 128, 0), pygame.Rect(player["pos"]["x"], player["pos"]["y"], 60, 60))
            clock.tick(60)

###INITIALIZE###
#runInParallel(client.online,mainLoop)
asyncio.get_event_loop().run_until_complete(mainLoop())
