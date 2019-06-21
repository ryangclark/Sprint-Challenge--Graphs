from player import Player
from room import Room
from roomgraphs import room_graphs
from world import World

from collections import deque
import random

# Load world
world = World()

roomGraph = room_graphs[5]

world.loadGraph(roomGraph)
world.printRooms()
player = Player("Name", world.startingRoom)


# FILL THIS IN
traversalPath = []
graph = dict()

player.currentRoom = world.startingRoom
r = -1
inverse_moves = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}

d = deque([[]])

next_direction = None
for direction in 'ews':
    if player.currentRoom.getRoomInDirection(direction):
        next_direction = direction
        break

while len(graph) < len(roomGraph) and r != player.currentRoom.id:
    next_direction = None
    adjacent_unvisited = 0
    r = player.currentRoom.id # anti-looping protocol

    # Cartography
    if player.currentRoom.id not in graph:
        graph[player.currentRoom.id] = {'n': '?', 's': '?', 'w': '?', 'e': '?'}
        
        for direction in 'news':
            adjacent = player.currentRoom.getRoomInDirection(direction)

            # Populate the map
            if adjacent:
                graph[player.currentRoom.id][direction] = adjacent.id
                # Set next direction to unexplored room
                if adjacent.id not in graph:
                    adjacent_unvisited += 1
                    next_direction = direction
            else:
                graph[player.currentRoom.id][direction] = adjacent
    else:
        for k, v in graph[player.currentRoom.id].items():
            if v and v not in graph:
                adjacent_unvisited += 1
                next_direction = k
                
    # Set next move
    if next_direction:
        if adjacent_unvisited > 1:
            d.append([next_direction])
        else:
            d[-1].append(next_direction)
        traversalPath.append(next_direction)
        player.travel(next_direction)
        continue
    else:
        breadcrumbs = d.pop() 
        while breadcrumbs:
            move = inverse_moves[breadcrumbs.pop()]
            traversalPath.append(move)
            player.travel(move)
        if not d:
            d.append([])
        continue


# TRAVERSAL TEST
visited_rooms = set()
player.currentRoom = world.startingRoom
visited_rooms.add(player.currentRoom.id)
for move in traversalPath:
    player.travel(move)
    visited_rooms.add(player.currentRoom.id)

if len(visited_rooms) == len(roomGraph):
    print(f"TESTS PASSED: {len(traversalPath)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(roomGraph) - len(visited_rooms)} unvisited rooms")
    print([i for i in range(len(roomGraph)) if i not in visited_rooms])

#######
# UNCOMMENT TO WALK AROUND
#######
# player.currentRoom.printRoomDescription(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     else:
#         print("I did not understand that command.")
