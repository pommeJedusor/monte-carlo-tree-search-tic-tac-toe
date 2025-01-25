import math
import random

FULL_GRID = 0b111_0111_0111

def get_empty_grid() -> int:
    return 0

def get_moves(p1: int, p2: int) -> list[tuple[int, int]]:
    grid = (p1 | p2) ^ FULL_GRID
    moves = []
    for i in range(11):
        if i % 4 == 3:continue
        if grid & (1 << i):
            moves.append((p2, p1 | (1 << i)))
    return moves

def toggle_move(player: int, move: int) -> int:
    return player ^ (1 << move)

def is_winning(player: int) -> bool:
    # horizontal
    if player & player >> 1 & player >> 2:
        return True
    # vertical
    if player & player >> 4 & player >> 8:
        return True
    # top left -> bottom right
    if player & player >> 5 & player >> 10:
        return True
    # top right -> bottom left
    if player & player >> 3 & player >> 6:
        return True
    return False

def is_draw(p1: int, p2: int) -> bool:
    return (p1 | p2) == FULL_GRID

class Node:
    def __init__(self, p1: int, p2: int, parent: "Node|None"=None):
        self.score = 0
        self.nb_visit = 0
        self.p1 = p1
        self.p2 = p2
        self.children: list[Node] = []
        self.parent = parent

def selection(node: Node) -> Node:
    if is_winning(node.p2):
        return node
    moves = get_moves(node.p1, node.p2)
    if len(moves) == 0:
        return node
    # selection
    if len(moves) == len(node.children):
        best_value = -1_000_000_000
        best_children = []
        for child in node.children:
            value = child.score / child.nb_visit + 1.4 * math.sqrt(math.log(node.nb_visit) / child.nb_visit)
            if value > best_value:
                best_children = [child]
                best_value = value
            elif value == best_value:
                best_children.append(child)
        return selection(random.choice(best_children))
    # expansion
    p1, p2 = moves[len(node.children)]
    child = Node(p1, p2, node)
    node.children.append(child)
    return child

def simulation(node: Node) -> int:
    p1, p2 = node.p1, node.p2
    nb_move = 0
    while not is_winning(p2) and not is_draw(p1, p2):
        p1, p2 = random.choice(get_moves(p1, p2))
        nb_move += 1

    if is_draw(p1, p2):
        return 0
    return ((nb_move + 1) % 2) * 2 - 1

def backpropagation(node: Node, score: int):
    if score > 1 or score < -1:
        print(score)
    node.score += score
    node.nb_visit += 1
    if node.parent:
        backpropagation(node.parent, -score)

def mcts(p1: int, p2: int) -> tuple[int, int]:
    root = Node(p1, p2)
    for _ in range(1_000):
        node = selection(root)
        score = simulation(node)
        backpropagation(node, score)

    moves: list[tuple[float, tuple[int, int]]] = []
    for child in root.children:
        moves.append((child.score / child.nb_visit, (child.p1, child.p2)))
    return max(moves)[1]

def show_grid(p1: int, p2: int):
    grid = [["_" for _ in range(3)] for _ in range(3)]
    for y in range(3):
        for x in range(3):
            if 1 << (y * 4 + x) & p1:
                grid[y][x] = "X"
            if 1 << (y * 4 + x) & p2:
                grid[y][x] = "O"
    for row in grid:
        print("".join(row))


p1, p2 = 0, 0
while not is_winning(p1) and not is_draw(p1, p2):
    p1, p2 = mcts(p1, p2)
    show_grid(p1, p2)
    print()
