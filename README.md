# server-client-architecture
Hey! I had an idea in my head for a server-client interaction pipeline for creating multiplayer games, and so here we are.
# What's going on?
What's happening is that there are 2 scripts: a client (`gamewindow.py`) and a server (`gameserver.py`) that talk to eachother right now through `localhost:6789`.
The `client` sends a packet containing a dict (`playerdict`) that contains all the information concerning the box the user controls (WASD).
The `server` recieves the packet, and updates `world` accordingly, with whatever new information is sent by the `client`.
The `server`, in turn, sends the client the `world` dictionary, allowing it to access all of the other players' positions and draw them to the screen.
