from spaced_repetition import storage
import os
import math


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

EOF_HOTKEY = 'ctrl+Z' if os.name == 'nt' else 'ctrl+D'


def main_loop():
    while True:
        clear_screen()
        print('Welcome to spaced-repetition-py!')
        print()
        print('1. Answer cards for today ('
              + str(len(storage.cards.today_cards_indexes)) + ' left)')
        print(f'2. Add a new card')
        print()
        print('9. Settings')
        print('0. Exit')
        print()
        try:
            run = input('')
        except:  # KeyboradInterrupt
            break
        try:
            run = int(run)
        except:  # incorrect input
            continue
        if run == 0:
            break
        if run == 1:
            answer_cards()
        if run == 2:
            add_a_new_card()
        if run == 9:
            settings()


def print_progress_bar(a, x):
    # a/x is completed
    sharp_count = math.ceil(25 * a / x)
    spaces_count = 25 - sharp_count
    print('[' + '#' * sharp_count + ' ' * spaces_count + ']')


def answer_cards():
    was = len(storage.cards.today_cards_indexes)
    now = was
    correct = 0
    for now in range(was, 0, -1):
        clear_screen()
        print_progress_bar(was - now, was)
        print()
        idx = storage.cards.pop_idx()
        card = storage.cards.all_cards[idx]
        print('=>', card.data['front'], '<=')
        print()
        try:
            input('Flip the card? ')
        except:  # KeyboradInterrupt
            break
        # redraw this screen
        clear_screen()
        print_progress_bar(was - now, was)
        print()
        print('=>', card.data['front'], '<=')
        print()
        print(card.data['back'])
        try:
            answer = input('(enter: accept, d: decline, smth else: skip): ')
        except:  # KeyboradInterrupt
            break
        if (answer == ''):
            card.check_as_right()
            correct += 1
        elif (answer == 'd'):
            card.check_as_wrong()
        else:
            continue
    clear_screen()
    print_progress_bar(1, 1)
    print()
    print("That's all for today!")
    if was > 0:
        print(f'Cards answered correctly: {correct}/{was}')
    print()

    try:
        input('Press enter to return to the menu ')
    except:  # KeyboradInterrupt
        pass


def add_a_new_card():
    while True:
        clear_screen()
        print('Adding a new card')
        print()
        try:
            front = input('Front side of the card: ')
        except:  # KeyboradInterrupt
            break
        print('Back side of the card (press ' + EOF_HOTKEY + ' to enter)')
        back = ''
        while True:
            try:
                line = input()
            except EOFError:
                break
            back += ('' if back == '' else '\n') + line
        storage.cards.add_from_dict({
                'front': front,
                'back': back,
                'level': 2,
                'date_wrong': storage.TODAY,
        })
        try:
            print()
            print('Card added. Press Enter to continue or ' + EOF_HOTKEY + ' to exit')
            input()
        except:  # KeyboradInterrupt
            break



def settings():
    input('TBD.. ')
    pass
