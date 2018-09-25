#eventhandler.py
import ast

def constructEvent(name,package):
    event = {}
    event["name"] = name
    event["package"] = package
    return str(event)

def example():
    print ("example event")

def worldUpdate(currentWorld,world):
    currentWorld["world"] = world
    return currentWorld

def playerUpdate(player,world):
    world["players"][player["name"]] = player
    return world

def handleEvent(event,world):
    ev = ast.literal_eval(event)
    res = None
    if ev["name"] == "test":
        example()
    if ev["name"] == "w-update":
        res = worldUpdate(world,ev["package"])
    if ev["name"] == "p-update":
        res = playerUpdate(ev["package"],world)
    return res
