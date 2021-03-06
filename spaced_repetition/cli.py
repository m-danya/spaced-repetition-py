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
        print(f'3. Watch my cards')
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
        if run == 3:
            watch_my_cards()
        if run == 9:
            settings()


def print_progress_bar(a, x):
    # a/x is completed
    if x == 0:
        print()
        return
    sharp_count = math.ceil(25 * a / x)
    spaces_count = 25 - sharp_count
    print('[' + '#' * sharp_count + ' ' * spaces_count + ']' + f' ({a}/{x})')


def answer_cards():
    was = len(storage.cards.today_cards_indexes)
    correct = 0
    incorrect = 0
    deleted = 0
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
            answer = input('(enter: accept, d: decline, x: remove permanently, smth else: skip): ')
        except:  # KeyboradInterrupt
            break
        if (answer == ''):
            card.check_as_right()
            correct += 1
        elif (answer == 'd'):
            card.check_as_wrong()
            incorrect += 1
        elif (answer == 'x'):
            card.mark_for_removal()
            deleted += 1
        else:
            continue
    clear_screen()
    print_progress_bar(was, was)
    print()
    print("That's all for today!")
    if was > 0:
        skipped = was - (correct + incorrect + deleted)
        skip_msg = ' ('
        if deleted > 0:
            skip_msg += f'+ {deleted} deleted'
            if skipped > 0:
                skip_msg += ', '
        if skipped > 0:
            skip_msg += f'+ {skipped} skipped'
        skip_msg += ')'
        if skip_msg == ' ()': 
            skip_msg = ''
        was = was - (skipped + deleted)
        print(f'Cards answered correctly: {correct}/{was}' + skip_msg)
    print()

    storage.cards.remove_unwanted_cards()
    storage.cards.save_to_file()

    storage.cards.get_cards_for_today()

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
            print('Card added. Press Enter to continue or ' +
                  EOF_HOTKEY + ' to exit')
            input()
        except:  # KeyboradInterrupt
            break


def settings():
    clear_screen()
    print('1. Change the `cards.json` location')
    print()
    print('0. Exit')
    print()
    try:
        choice = input('')
    except:  # KeyboradInterrupt
        pass
    if choice == '1':
        try:
            new_path = input('Type the new path (it must be absolute): ')
            storage.config.change_cards_path_and_save(new_path)
            storage.config.load_from_file()
            storage.cards.load_from_file()
        except:  # KeyboradInterrupt
            pass


def watch_my_cards():
    clear_screen()
    print('You have ' +
            f'{len(storage.CardsStorage.all_cards)} cards in your system, wow!')
    print()
    for i, card in enumerate(storage.cards.all_cards):
        print(f"{i + 1}) {card.data['front']}")
    try:
        print()
        print('That\'s all. Press Enter to exit')
        input()
    except:  # KeyboradInterrupt
        pass

    
