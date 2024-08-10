import os
import json
class AI_Model():
    def __init__(self,name) -> None:
        self.number_of_training_loops=None
        self.number_of_training_loops_against_human=None
        self.number_of_training_loops_against_ai_model=None
        self.number_of_training_loops_against_test_algorithm=None
        self.wins=None
        self.losses=None
        self.ties=None

        self.modelname=name

        self.parent_dir = "data/models"
        self.name_config_file = "/modelconfig.json"
        self.initial_json_data = {'training loops': 0,
                     "training loops against Human": 0,
                     "training loops against AI-Model": 0,
                     "training loops against Test Algorithm": 0,
                     
                     "losses": 0,
                     "wins": 0,
                     "ties": 0
                     }

        self.directory = self.modelname
        self.path = os.path.join(self.parent_dir, self.directory)

    def get_total_number_of_training_loops(self):
        if self.number_of_training_loops is None:
            try:
                if os.path.exists("data/models/" + self.modelname + self.name_config_file):
                    with open("data/models/" + self.modelname + self.name_config_file, "r") as file:
                        data = json.load(file)
                        return data["training loops"]
                else:
                    return 0
            except PermissionError:
                print("Please close the file and try again")
        else:
            return self.number_of_training_loops

    def log_number_of_training_loops(self,opponent):
        if os.path.exists("data/models/" + self.modelname + self.name_config_file):
            with open("data/models/" + self.modelname + self.name_config_file, "r") as file:
                data = json.load(file)
                data["training loops"] += 1
                self.number_of_training_loops = data["training loops"]
                data["training loops against "+opponent] += 1
                if opponent=="Human":
                    self.number_of_training_loops_against_human = data["training loops against Human"]
                elif opponent=="AI-Model":
                    self.number_of_training_loops_against_ai_model = data["training loops against AI-Model"]
                elif opponent=="Test Algorithm":
                    self.number_of_training_loops_against_test_algorithm = data["training loops against Test Algorithm"]
                with open("data/models/" + self.modelname + self.name_config_file, "w") as file:
                    json.dump(data, file, sort_keys = True, indent = 4, ensure_ascii = False)
        else:
            raise Exception("Config file not found, try to delete the model and create it again, or replace the config file with the template file")
    
    def log_win(self):
        if os.path.exists("data/models/" + self.modelname + self.name_config_file):
            with open("data/models/" + self.modelname + self.name_config_file, "r") as file:
                data = json.load(file)
                data["wins"] += 1
                self.wins = data["wins"]
                with open("data/models/" + self.modelname + self.name_config_file, "w") as file:
                    json.dump(data, file, sort_keys = True, indent = 4, ensure_ascii = False)
        else:
            raise Exception("Config file not found, try to delete the model and create it again, or replace the config file with the template file")
    def log_loss(self):
        if os.path.exists("data/models/" + self.modelname + self.name_config_file):
            with open("data/models/" + self.modelname + self.name_config_file, "r") as file:
                data = json.load(file)
                data["losses"] += 1
                self.losses = data["losses"]
                with open("data/models/" + self.modelname + self.name_config_file, "w") as file:
                    json.dump(data, file, sort_keys = True, indent = 4, ensure_ascii = False)
        else:
            raise Exception("Config file not found, try to delete the model and create it again, or replace the config file with the template file")

    def log_tie(self):
        if os.path.exists("data/models/" + self.modelname + self.name_config_file):
            with open("data/models/" + self.modelname + self.name_config_file, "r") as file:
                data = json.load(file)
                data["ties"] += 1
                self.ties = data["ties"]
                with open("data/models/" + self.modelname + self.name_config_file, "w") as file:
                    json.dump(data, file, sort_keys = True, indent = 4, ensure_ascii = False)
        else:
            raise Exception("Config file not found, try to delete the model and create it again, or replace the config file with the template file")

    def get_number_of_wins(self):
        if self.wins is None:
            try:
                if os.path.exists("data/models/" + self.modelname + self.name_config_file):
                    with open("data/models/" + self.modelname + self.name_config_file, "r") as file:
                        data = json.load(file)
                        return data["wins"]
                else:
                    return 0
            except PermissionError:
                print("Please close the file and try again")
        else:
            return self.wins
    def get_number_of_losses(self):
        if self.losses is None:
            try:
                if os.path.exists("data/models/" + self.modelname + self.name_config_file):
                    with open("data/models/" + self.modelname + self.name_config_file, "r") as file:
                        data = json.load(file)
                        return data["losses"]
                else:
                    return 0
            except PermissionError:
                print("Please close the file and try again")
        else:
            return self.losses

    def get_number_of_ties(self):
        if self.ties is None:
            try:
                if os.path.exists("data/models/" + self.modelname + self.name_config_file):
                    with open("data/models/" + self.modelname + self.name_config_file, "r") as file:
                        data = json.load(file)
                        return data["ties"]
                else:
                    return 0
            except PermissionError:
                print("Please close the file and try again")
        else:
            return self.ties

    def reset_stats(self):
        with open(self.path + self.name_config_file, 'w') as out_file:
            json.dump(self.initial_json_data, out_file, sort_keys = True, indent = 4, ensure_ascii = False)
        
        print("The stats of the model " + self.modelname + " have been reset")
    
    def reset_end_states(self):
        with open(self.path + self.name_config_file, 'r+') as file:
            json_data = json.load(file)
            json_data["losses"] = 0
            json_data["wins"] = 0
            json_data["ties"] = 0
            file.seek(0)
            json.dump(json_data, file, sort_keys = True, indent = 4, ensure_ascii = False)
            print("updated values:",json_data)
            file.truncate()
        print("The end states of the model " + self.modelname + " have been reset")


