import os
import json
import gomoku
class AI_model():
    def __init__(self) -> None:
        self.number_of_training_loops=0
        self.number_of_training_loops_against_human=0
        self.number_of_training_loops_against_ai_model=0
        self.number_of_training_loops_against_test_algorithm=0
        self.wins=0
        self.losses=0
        self.ties=0
    
    def get_total_number_of_training_loops(self,modelname):
        try:
            if os.path.exists("data/models/" + modelname + self.name_config_file):
                with open("data/models/" + modelname + self.name_config_file, "r") as file:
                    data = json.load(file)
                    return data["training loops"]
            else:
                return 0
        except PermissionError:
            print("Please close the file and try again")

    def log_number_of_training_loops(self, modelname,opponent):
        if os.path.exists("data/models/" + modelname + self.name_config_file):
            with open("data/models/" + modelname + self.name_config_file, "r") as file:
                data = json.load(file)
                data["training loops"] += 1
                data["training loops against "+opponent] += 1
                with open("data/models/" + modelname + self.name_config_file, "w") as file:
                    json.dump(data, file, sort_keys = True, indent = 4, ensure_ascii = False)
        else:
            raise Exception("Config file not found, try to delete the model and create it again, or replace the config file with the template file")
    
    def log_win(self, modelname):
        if os.path.exists("data/models/" + modelname + self.name_config_file):
            with open("data/models/" + modelname + self.name_config_file, "r") as file:
                data = json.load(file)
                data["wins"] += 1
                with open("data/models/" + modelname + self.name_config_file, "w") as file:
                    json.dump(data, file, sort_keys = True, indent = 4, ensure_ascii = False)
        else:
            raise Exception("Config file not found, try to delete the model and create it again, or replace the config file with the template file")
    def log_loss(self, modelname):
        if os.path.exists("data/models/" + modelname + self.name_config_file):
            with open("data/models/" + modelname + self.name_config_file, "r") as file:
                data = json.load(file)
                data["losses"] += 1
                with open("data/models/" + modelname + self.name_config_file, "w") as file:
                    json.dump(data, file, sort_keys = True, indent = 4, ensure_ascii = False)
        else:
            raise Exception("Config file not found, try to delete the model and create it again, or replace the config file with the template file")

    def log_tie(self):
        list_AI_players = [p for p in gomoku.players if p.TYPE == "AI-Model"]

        for player in list_AI_players:
            modelname=player.model_name
            if os.path.exists("data/models/" + modelname + self.name_config_file):
                with open("data/models/" + modelname + self.name_config_file, "r") as file:
                    data = json.load(file)
                    data["ties"] += 1
                    with open("data/models/" + modelname + self.name_config_file, "w") as file:
                        json.dump(data, file, sort_keys = True, indent = 4, ensure_ascii = False)
            else:
                raise Exception("Config file not found, try to delete the model and create it again, or replace the config file with the template file")

    def get_number_of_wins(self, modelname):
        try:
            if os.path.exists("data/models/" + modelname + self.name_config_file):
                with open("data/models/" + modelname + self.name_config_file, "r") as file:
                    data = json.load(file)
                    return data["wins"]
            else:
                return 0
        except PermissionError:
            print("Please close the file and try again")
    def get_number_of_losses(self, modelname):
        try:
            if os.path.exists("data/models/" + modelname + self.name_config_file):
                with open("data/models/" + modelname + self.name_config_file, "r") as file:
                    data = json.load(file)
                    return data["losses"]
            else:
                return 0
        except PermissionError:
            print("Please close the file and try again")

    def get_number_of_ties(self, modelname):
        try:
            if os.path.exists("data/models/" + modelname + self.name_config_file):
                with open("data/models/" + modelname + self.name_config_file, "r") as file:
                    data = json.load(file)
                    return data["ties"]
            else:
                return 0
        except PermissionError:
            print("Please close the file and try again")

    def reset_stats(self, modelName):
         # Directory 
        directory = modelName

        path = os.path.join(self.parent_dir, directory) 

        with open(path + self.name_config_file, 'w') as out_file:
            json.dump(self.initial_json_data, out_file, sort_keys = True, indent = 4, ensure_ascii = False)
        
        print("The stats of the model " + modelName + " have been reset")
    
    def reset_end_states(self, modelName):
         # Directory 
        directory = modelName

        path = os.path.join(self.parent_dir, directory) 

        with open(path + self.name_config_file, 'r+') as file:
            json_data = json.load(file)
            json_data["losses"] = 0
            json_data["wins"] = 0
            json_data["ties"] = 0
            file.seek(0)
            json.dump(json_data, file, sort_keys = True, indent = 4, ensure_ascii = False)
            print("updated values:",json_data)
            file.truncate()
        print("The end states of the model " + modelName + " have been reset")


