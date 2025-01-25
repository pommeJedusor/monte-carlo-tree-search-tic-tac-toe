from mcts import mcts, show_grid, is_draw, is_winning

MAPPING = {"1": 0, "2": 1, "3": 2, "4": 4, "5": 5, "6": 6, "7": 8, "8": 9, "9": 10}

answer = input("do you want to start? y/n ")
is_player_first = answer.lower() == "y"
p1 = 0
p2 = 0
turn = 0
while not is_winning(p2) and not is_draw(p1, p2):
    if turn % 2 == 0 and is_player_first or turn % 2 == 1 and not is_player_first:
        show_grid(p1, p2)
        answer = "pomme"
        while not answer in MAPPING or 1 << MAPPING[answer] & (p1 | p2):
            if answer != "pomme":
                print("move's not valid")
            answer = input("choose a move: ")
        p1 |= 1 << MAPPING[answer]
        p1, p2 = p2, p1
    else:
        show_grid(p2, p1)
        print()
        p1, p2 = mcts(p1, p2)
    turn += 1

show_grid(p2, p1)
if is_winning(p2):
    print("-- You lost --")
elif is_draw(p1, p2):
    print("-- Tie --")
