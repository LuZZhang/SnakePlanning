import random
from typing import List, Dict

"""
This file can be a nice home for your move logic, and to write helper functions.

We have started this for you, with a function to help remove the 'neck' direction
from the list of possible moves!
"""


def avoid_my_neck(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str]) -> List[str]:
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with the 'neck' direction removed
    """
    my_neck = my_body[1]  # The segment of body right after the head is the 'neck'

    if my_neck["x"] < my_head["x"]:  # my neck is left of my head
        possible_moves.remove("left")
    elif my_neck["x"] > my_head["x"]:  # my neck is right of my head
        possible_moves.remove("right")
    elif my_neck["y"] < my_head["y"]:  # my neck is below my head
        possible_moves.remove("down")
    elif my_neck["y"] > my_head["y"]:  # my neck is above my head
        possible_moves.remove("up")

    return possible_moves

def avoid_boundry(board, head, moves):
    print("before avoid_boundry", moves)
    left = 0
    right = board['width'] - 1
    bottom = 0
    top = board['height'] - 1
    moves = set(moves)
    if 'left' in moves and head['x'] == left: moves.remove('left')
    if 'right' in moves and head['x'] == right: moves.remove('right')
    if 'down' in moves and head['y'] == bottom: moves.remove('down')
    if 'up' in moves and head['y'] == top: moves.remove('up')
    return list(moves)


def avoid_snake(snakes, head, moves):
    print("before avoid_snake", moves)
    moves = set(moves)
    for snake in snakes:
        snake_body = snake['body']
        snake_body = snake_body[:len(snake_body) - 1]
        for body in snake_body:
            if 'left' in moves and body['x'] == head['x'] - 1 and body['y'] == head['y']: moves.remove('left')
            if 'right' in moves and body['x'] == head['x'] + 1 and body['y'] == head['y']: moves.remove('right')
            if 'down' in moves and body['x'] == head['x'] and body['y'] == head['y'] - 1: moves.remove('down')
            if 'up' in moves and body['x'] == head['x'] and body['y'] == head['y'] + 1: moves.remove('up')
    return list(moves)


def avoid_body(body, head, moves):
    print("before avoid_body", moves)
    moves = set(moves)
    bodys = body[:len(body) - 1]
    for body in bodys:
        if 'left' in moves and body['x'] == head['x'] - 1 and body['y'] == head['y']: moves.remove('left')
        if 'right' in moves and body['x'] == head['x'] + 1 and body['y'] == head['y']: moves.remove('right')
        if 'down' in moves and body['x'] == head['x'] and body['y'] == head['y'] - 1: moves.remove('down')
        if 'up' in moves and body['x'] == head['x'] and body['y'] == head['y'] + 1: moves.remove('up')
    return list(moves)


def avoid_hazards(hazards, head, moves):
    moves = set(moves)
    for hazard in hazards:
        if 'left' in moves and hazard['x'] == head['x'] - 1 and hazard['y'] == head['y']: moves.remove('left')
        if 'right' in moves and hazard['x'] == head['x'] + 1 and hazard['y'] == head['y']: moves.remove('right')
        if 'down' in moves and hazard['x'] == head['x'] and hazard['y'] == head['y'] - 1: moves.remove('down')
        if 'up' in moves and hazard['x'] == head['x'] and hazard['y'] == head['y'] + 1: moves.remove('up')
    return list(moves)


def greedy(foods, head, moves):
    nxts = []
    for move in moves:
        if move == 'left': nxts.append((head['x'] - 1, head['y'], 'left'))
        if move == 'right': nxts.append((head['x'] + 1, head['y'], 'right'))
        if move == 'down': nxts.append((head['x'], head['y'] - 1, 'down'))
        if move == 'up': nxts.append((head['x'], head['y'] + 1, 'up'))
    best = float("inf")
    final = set([])
    for food in foods:
        good = float("inf")
        picks = set([])
        for nxt in nxts:
            dis = abs(nxt[0] - food['x']) + abs(nxt[1] - food['y'])
            if dis < good:
                picks = {nxt[2]}
                good = dis
            elif dis == good:
                picks.add(nxt[2])
        if good < best:
            final = picks
            best = good
        elif good == best:
            final = final.union(picks)
    return list(final)




def cost(food, board, head):
    harzards = board['harzards']
    snakes = board['snakes']
    def dfs(head, food, c):
        nonlocal harzards, snakes
        if food['x'] == head['x'] and food['y'] == head['y']: return c
        moves = ["up", "down", "left", "right"]
        moves = avoid_snake(snakes, head, moves)
        moves = avoid_boundry(board, head, moves)
        moves = avoid_hazards(harzards, head, moves)
        nxt = []
        actions = []
        for move in moves:
            if 'left' == move:
                dic = {'x': head['x'] - 1, 'y': head['y']}
                nxt.append(dfs(dic, food, c + 1))
                actions.append('left')
            if 'right' == move:
                dic = {'x': head['x'] + 1, 'y': head['y']}
                nxt.append(dfs(dic, food, c + 1))
                actions.append('right')
            if 'down' == move:
                dic = {'x': head['x'], 'y': head['y'] - 1}
                nxt.append(dfs(dic, food, c + 1))
                actions.append('down')
            if 'up' == move:
                dic = {'x': head['x'], 'y': head['y'] + 1}
                nxt.append(dfs(dic, food, c + 1))
                actions.append('up')
        return nxt.index(min(nxt))
    return dfs(head, food, 0)



def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    my_head = data["you"]["head"]  # A dictionary of x/y coordinates like {"x": 0, "y": 0}
    my_body = data["you"]["body"]  # A list of x/y coordinate dictionaries like [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    yself = data['you']['id']
    board = data['board']
    snakes = [snake for snake in board['snakes'] if snake['id'] != yself]
    foods = board['food']

    # TODO: uncomment the lines below so you can see what this data looks like in your output!
    print(f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~")
    print(f"All board data this turn: {data}")
    print(f"My Battlesnakes head this turn is: {my_head}")
    print(f"My Battlesnakes body this turn is: {my_body}")

    possible_moves = ["up", "down", "left", "right"]

    # Don't allow your Battlesnake to move back in on it's own neck
    possible_moves = avoid_my_neck(my_head, my_body, possible_moves)

    # TODO: Using information from 'data', find the edges of the board and don't let your Battlesnake move beyond them
    # board_height = ?
    # board_width = ?
    possible_moves = avoid_boundry(board, my_head, possible_moves)

    # TODO Using information from 'data', don't let your Battlesnake pick a move that would hit its own body
    possible_moves = avoid_body(my_body, my_head, possible_moves)

    # TODO: Using information from 'data', don't let your Battlesnake pick a move that would collide with another Battlesnake
    possible_moves = avoid_snake(snakes, my_head, possible_moves)

    # If not moves could choose or no foods currently, randomly choose a action.
    if not possible_moves or not foods: return random.choice(["up", "down", "left", "right"])

    # TODO: Using information from 'data', make your Battlesnake move towards a piece of food on the board
    possible_moves = greedy(foods, my_head, possible_moves)

    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    move = random.choice(possible_moves)


    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move
