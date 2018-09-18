import pygame
from multiprocessing import Process
import asyncio
import websockets
import ast
import json

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
movement = {pygame.K_w: ( 0, -1),
            pygame.K_s: ( 0,  1),
            pygame.K_a: (-1,  0), 
            pygame.K_d: ( 1,  0)}
with open('config.json') as f:
    data = json.load(f)


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
    global data
    speed = 5
    square = 60
    direction = [0,0]
    tempdict = playerdict.copy()
    myfont = pygame.font.SysFont("monospace", 15)
    done = False
    while not done:
            w, h = pygame.display.get_surface().get_size()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    #direction = (0,0)
                  if event.key == pygame.K_w:
                    direction[1] = -1
                  if event.key == pygame.K_s:
                    direction[1] = 1
                  if event.key == pygame.K_a:
                    direction[0] = -1
                  if event.key == pygame.K_d:
                    direction[0] = 1
                    #direction = movement.get(event.key,direction)
                if event.type == pygame.KEYUP:
                  if event.key == pygame.K_w or event.key == pygame.K_s:
                    direction[1] = 0
                  if event.key == pygame.K_a or event.key == pygame.K_d:
                    direction[0] = 0
                
            playerdict["pos"]["x"] = playerdict["pos"]["x"] + (direction[0]*speed)
            playerdict["pos"]["y"] = playerdict["pos"]["y"] + (direction[1]*speed)
            pygame.display.flip()
            screen.fill((255, 255, 255))
            async with websockets.connect('ws://'+data["server"]+':12250') as websocket:
                await websocket.send(str(playerdict))
                dat = await websocket.recv()
                raw =  ast.literal_eval(dat)
                #print(raw)
                for name,player in raw["players"].items():
                    #print ("player",name,player)
                    if not name == playerdict["name"]:
                        pygame.draw.rect(screen, (255, 128, 0), pygame.Rect(player["pos"]["x"]-playerdict["pos"]["x"]-square/2, player["pos"]["y"]-playerdict["pos"]["y"]-square/2, square, square))
                        label = myfont.render(name, 1, (0,0,0))
                        screen.blit(label, (player["pos"]["x"]-playerdict["pos"]["x"]-square/2, player["pos"]["y"]-playerdict["pos"]["y"]-square/2))
            #print(w,h)
            pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(w/2-square/2, h/2-square/2, square, square)) #player
            clock.tick(60)

###INITIALIZE###
#runInParallel(client.online,mainLoop)
asyncio.get_event_loop().run_until_complete(mainLoop())
