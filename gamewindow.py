import pygame
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
movement = {pygame.K_w:    ( 0, -1),
            pygame.K_s:  ( 0,  1),
            pygame.K_a:  (-1,  0), 
            pygame.K_d: ( 1,  0)}

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
    global movement
    direction = (0,0)
    tempdict = playerdict.copy()
    myfont = pygame.font.SysFont("monospace", 15)
    done = False
    while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    #direction = (0,0)
                    direction = movement.get(event.key,direction)
                if event.type == pygame.KEYUP:
                    direction = (0,0)
                
            playerdict["pos"]["x"] = playerdict["pos"]["x"] + direction[0]
            playerdict["pos"]["y"] = playerdict["pos"]["y"] + direction[1]
            pygame.display.flip()
            screen.fill((255, 255, 255))
            pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(playerdict["pos"]["x"], playerdict["pos"]["y"], 60, 60))
            async with websockets.connect('ws://localhost:6789') as websocket:
                await websocket.send(str(playerdict))
                dat = await websocket.recv()
                raw =  ast.literal_eval(dat)
                #print(raw)
                for name,player in raw["players"].items():
                    #print ("player",name,player)
                    if not name == playerdict["name"]:
                        pygame.draw.rect(screen, (255, 128, 0), pygame.Rect(player["pos"]["x"], player["pos"]["y"], 60, 60))
                        label = myfont.render(name, 1, (255,255,255))
                        screen.blit(label, (player["pos"]["x"], player["pos"]["y"]))
            clock.tick(60)

###INITIALIZE###
#runInParallel(client.online,mainLoop)
asyncio.get_event_loop().run_until_complete(mainLoop())
