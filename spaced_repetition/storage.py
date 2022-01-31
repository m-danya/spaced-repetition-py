from pathlib import Path
import configparser
from datetime import date, timedelta
import random
import json

SRS_LEVEL_TO_DAYS = {
    1: 0,
    2: 1,
    3: 3,
    4: 8,
    5: 19,
    6: 44,
    7: 100,
    8: 226,
    9: 510,
    10: 1149,
    11: 2561,
    12: 5568,
    13: 11669,
    14: 23422,
    15: 44954
}

TODAY = date.today()


class Config:
    settings = {}

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_file = Path(__file__).parent / 'config.ini'
        pass

    def load_from_file(self):

        if self.config_file.exists():
            # use existing settings
            with open(self.config_file, "r") as f:
                self.config.read_file(f)
        else:
            # set default settings
            default_data_folder = Path(__file__).parent / 'data'
            default_data_folder.mkdir(exist_ok=True, parents=True)

            self.config.add_section("Settings")
            self.change_cards_path_and_save(str(default_data_folder))

        # move read settings to self.settings
        self.settings = {
            "cards_path": Path(self.config["Settings"]["cards_path"])
        }

        if not self.settings['cards_path'].exists():
            print('Warning: Creating an empty data folder, because it does not exist')
            self.settings['cards_path'].mkdir(exist_ok=True, parents=True)
        cards_file = self.settings['cards_path'] / "cards.json"
        if not cards_file.exists():
            cards_file.touch()
    
    def change_cards_path_and_save(self, new_path):
        self.config["Settings"]["cards_path"] = new_path
        self.settings["cards_path"] = Path(new_path)

        with open(self.config_file, "w") as f:
            self.config.write(f)


class Card:
    data = {}
    need_to_be_removed = False

    def __init__(self, data):
        self.data = data

    def is_for_today(self):
        return self.data['date_next'] <= TODAY

    def recalculate_next_date(self):
        add_days = SRS_LEVEL_TO_DAYS.get(self.data['level'], 10000)
        self.data['date_next'] = self.data['date_wrong'] + \
            timedelta(days=add_days)

    def check_as_wrong(self):
        self.data['date_wrong'] = date.today()
        self.data['level'] = 2
        self.recalculate_next_date()

    def check_as_right(self):
        while self.is_for_today():
            self.data['level'] += 1
            self.recalculate_next_date()

    def mark_for_removal(self):
        self.need_to_be_removed = True


class CardsStorage:
    all_cards = []
    today_cards_indexes = []

    def __init__(self):
        pass

    def add_from_dict(self, d):
        card = Card(d)
        card.recalculate_next_date()
        self.all_cards.append(card)
        self.save_to_file()

    def save_to_file(self):
        cards_file = config.settings['cards_path'] / 'cards.json'
        with open(cards_file, 'w') as f:
            json.dump([x.data for x in self.all_cards], f, default=str)

    def get_cards_for_today(self):
        self.today_cards_indexes.clear()
        for i, card in enumerate(self.all_cards):
            if card.is_for_today():
                self.today_cards_indexes.append(i)
        random.shuffle(self.today_cards_indexes)

    def load_from_file(self):
        self.all_cards.clear()
        cards_file = config.settings['cards_path'] / 'cards.json'
        cards_loaded = []
        with open(cards_file, 'r') as f:
            try:
                cards_loaded = json.load(f)
            except:
                print('empty json!')
        for c in cards_loaded:
            card = Card({
                'front': c['front'],
                'back': c['back'],
                'level': c['level'],
                'date_wrong': date.fromisoformat(c['date_wrong']),
                'date_next': date.fromisoformat(c['date_next'])
            })
            self.all_cards.append(card)
        cards.get_cards_for_today()

    def pop_idx(self):
        return self.today_cards_indexes.pop()

    def remove_unwanted_cards(self):
        self.all_cards = [card for card in self.all_cards if not card.need_to_be_removed]

config = Config()
cards = CardsStorage()
