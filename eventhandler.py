#eventhandler.py
import ast

#TODO: more efficient world updates- world can get big, so only pass and recieve what has changed
def constructEvent(name,package):
    event = {}
    event["name"] = name
    event["package"] = package
    return str(event)

def example():
    print ("example event")

def getFullWorld(world):
    return world

def worldUpdate(currentWorld,world):
    currentWorld.update(world)
    return currentWorld

def playerUpdate(player,world):
    world["players"][player["name"]] = player
    return world

def handleEvent(event,world):
    ev = ast.literal_eval(event)
    res = None
    if ev["name"] == "example":
        example()
    if ev["name"] == "w-update":
        res = worldUpdate(world,ev["package"])
    if ev["name"] == "p-update":
        res = playerUpdate(ev["package"],world)
    if ev["name"] == "init_world":
        res = getFullWorld(ev["package"])
    return res
