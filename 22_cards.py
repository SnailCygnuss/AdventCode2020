import time
from collections import deque
import itertools


def calculate_score(player_cards: deque) -> int :
    player_cards.reverse()
    tot_val = 0
    for val, card in enumerate(player_cards, start=1):
        tot_val += val * card
    return tot_val


def play_game(player1: deque, player2: deque) -> int :
    score = 0

    while len(player1) != 0 and len(player2) != 0:
        card1 = player1[0]
        card2 = player2[0]

        if card1 > card2:
            player1.extend([card1, card2])
        elif card2 > card1:
            player2.extend([card2, card1])
        player1.popleft()
        player2.popleft()

    if len(player1) == 0:
        print('Player 2 is winner')
        score = calculate_score(player2)
    elif len(player2) == 0:
        print('Player 1 is winner')
        score = calculate_score(player1)

    return score 


def play_recursive_combat2(player1: deque, player2: deque):

    seen = set()
    
    score = 0
    while True:
        p1_hash = ''.join(map(str, player1))
        p2_hash = ''.join(map(str, player2))
        uid = p1_hash + '0' + p2_hash
        if uid in seen:
            winner = 1
            break
        else:
            seen.add(uid)
        
        c1 =player1.popleft()
        c2 =player2.popleft()

        if len(player1) >= c1 and len(player2) >= c2:
            sub_winner, _ = play_recursive_combat2(deque([player1[x] for x in range(c1)]), deque([player2[x] for x in range(c2)]))
            if sub_winner == 1:
                player1.extend([c1, c2])
            else:
                player2.extend([c2, c1])
        else:
            if c1 > c2:
                player1.extend([c1, c2])
            else:
                player2.extend([c2, c1])
        
        if len(player1) == 0:
            winner = 2
            score = calculate_score(player2)
            break
        elif len(player2) == 0:
            winner = 1
            score = calculate_score(player1)
            break

    return winner, score


def main(file_name='Day_22/22_input.txt'):
    player1_cards = []
    player2_cards = []
    with open(file_name, 'r') as f:
        line = f.readline()
        while line != '':
            if line.startswith('Player 1'):
                line = f.readline()
                while line not in ['\n', '']:
                    player1_cards.append(int(line.strip()))
                    line = f.readline()
            elif line.startswith('Player 2'):
                line = f.readline()
                while line not in ['\n', '']:
                    player2_cards.append(int(line.strip()))
                    line = f.readline()
            line = f.readline()

    player1_deque = deque(player1_cards)
    player2_deque = deque(player2_cards)
    score = play_game(player1_deque.copy(), player2_deque.copy())
    print(f'Score: {score}')

    # Second Game
    winner, score = play_recursive_combat2(player1_deque, player2_deque)
    print(f'Winner of recursive combat is Player{winner}')
    print(f'Score: {score}')


def testcase():
    print('Test Case')
    main(file_name='day_22/22_test.txt')


if __name__ == '__main__':
    start1 = time.time()
    # testcase()
    main()
    print(f'Part one finished in {time.time() - start1}')