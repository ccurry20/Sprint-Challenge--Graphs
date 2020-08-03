from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# move the player:
def move_player(direction):
    player.travel(direction) # check players direction options
    # keep adding to traversal path
    traversal_path.append(direction) # n, n, 

# DFT traversal
def DFT_recursive(visited=None, prev=None, move=None):
    current_room = player.current_room.id # grab the current room
    # grab all possible EXITS for current room
    neighbors = player.current_room.get_exits() 
    reverse = {'w': 'e', 'n': 's', 's': 'n', 'e': 'w'}

    if visited == None:
         visited = {}

    # current room is not in visited, add to visited
    if current_room not in visited: 
        visited[current_room] = {}

    # if there is direction (move) add to visited as current node (vertex)
    if move is not None: 
        visited[prev][move] = current_room

    if prev is not None: # if prev was 'N' reverse must be 'S'
        visited[current_room][reverse[move]] = prev # add reverse to visited direction

    if len(visited[current_room]) < len(neighbors): # if visited current has more exits
        for direction in neighbors: # 'n', 's', 'e', 'w' possible exits
            if direction not in visited[current_room]: # if direction to move not in current room
                move_player(direction) # move player to that direction and add to traversal path
                DFT_recursive(visited, prev=current_room, move=direction) #recurse

    if len(visited) < len(room_graph): # if more roooms
        direction = reverse[move]
        move_player(direction)

DFT_recursive() # invoke function with default


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
