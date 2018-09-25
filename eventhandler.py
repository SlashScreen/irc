#eventhandler.py
def example():
    print ("example event")

def worldUpdate(currentWorld,world):
    currentWorld["world"] = world
    return currentWorld

def playerUpdate(player,world):
    world["players"][player["name"]] = player
    return world

def handleEvent(event,world):
    res = None
    if event["name"] = "test":
        example()
    if event["name"] = "w-update":
        worldUpdate(world,event["package"])
    if event["name"] = "p-update":
        playerUpdate(event["package"],world)
