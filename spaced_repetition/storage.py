from pathlib import Path
import configparser


class Config:
    settings = { }

    def __init__(self):
        self.read_from_file()
    
    def read_from_file(self):
        config = configparser.ConfigParser()
        config_file = Path(__file__).parent / 'config.ini'

        if config_file.exists():
            # use existing settings
            with open(config_file, "r") as f:
                config.read_file(f)
        else:
            # set default settings
            default_data_folder = Path(__file__).parent / 'data'
            default_data_folder.mkdir(exist_ok=True, parents=True)

            config.add_section("Settings")
            config["Settings"]["cards_path"] = str(default_data_folder)
            
            with open(config_file, "w") as f:
                config.write(f)

        # move read settings to self.settings
        self.settings = {
                "cards_path": Path(config["Settings"]["cards_path"])
        }

        if not self.settings['cards_path'].exists():
            print('Warning: Creating an empty data folder, because it does not exist')
            self.settings['cards_path'].mkdir(exist_ok=True, parents=True)
        print('data folder: ', self.settings['cards_path'])
        
config = Config()