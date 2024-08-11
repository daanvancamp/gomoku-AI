import os
import json
class AI_Model():
    def __init__(self,name,training) -> None:
        self.training=training

        self.number_of_training_loops=None
        self.number_of_training_loops_against_human=None
        self.number_of_training_loops_against_ai_model=None
        self.number_of_training_loops_against_test_algorithm=None
        self.wins=None
        self.losses=None
        self.ties=None

        self.initial_json_data = {

                     "training stats": {
                         'training loops': 0,
                         "training loops against Human": 0,
                         "training loops against AI-Model": 0,
                         "training loops against Test Algorithm": 0},

                     "total end stats" :{
                         "losses": 0,
                         "wins": 0,
                         "ties": 0},
                     "games end stats":{
                         "wins":0,
                         "losses":0,
                         "ties":0},

                     "training loops end stats":{
                         "wins":0,
                         "losses":0,
                         "ties":0}

                     }
        
        self.parent_dir = "data/models"
        self.name_config_file = "/modelconfig.json"
        self.modelname=name
        self.directory = self.modelname
        self.path = os.path.join(self.parent_dir, self.directory)
        self.path_config_file=self.path+self.name_config_file
    
    def add_one_to_value_from_config_file(self,category,item):
        if os.path.exists(self.path_config_file):
            try:
                with open(self.path_config_file, "r") as file:
                    data = json.load(file)
                    data[category][item] += 1
                    with open(self.path_config_file, "w") as file:
                        json.dump(data, file, sort_keys = True, indent = 4, ensure_ascii = False)
            except PermissionError:
                print("Please close the file and try again")
        else:
            raise Exception("Config file not found, try to delete the model and create it again, or replace the config file with the template file")

    def get_value_from_config_file(self,category,item):
        if os.path.exists(self.path_config_file):
            try:
                with open(self.path_config_file, "r") as file:
                    data = json.load(file)
                    return data[category][item]
            except PermissionError:
                print("Please close the file and try again")
        else:
            raise Exception("Config file not found, try to delete the model and create it again, or replace the config file with the template file")

    def get_number_of_training_loops(self):
        if self.number_of_training_loops is None:
            return self.get_value_from_config_file("training stats","training loops")
        else:
            return self.number_of_training_loops

    def log_number_of_training_loops(self,opponent):
        self.add_one_to_value_from_config_file("training stats","training loops")
        self.number_of_training_loops = self.get_value_from_config_file("training stats","training loops")
        self.add_one_to_value_from_config_file("training stats","training loops against "+ opponent)
        if opponent=="Human":
            self.number_of_training_loops_against_human = self.get_value_from_config_file("training stats","training loops against Human")
        elif opponent=="AI-Model":
            self.number_of_training_loops_against_ai_model = self.get_value_from_config_file("training stats","training loops against AI-Model")
        elif opponent=="Test Algorithm":
            self.number_of_training_loops_against_test_algorithm = self.get_value_from_config_file("training stats","training loops against Test Algorithm")
    
    def log_win(self):
        self.add_one_to_value_from_config_file("total end stats","wins")
        self.wins = self.get_value_from_config_file("total end stats","wins")
                
    def log_loss(self):
        self.add_one_to_value_from_config_file("total end stats","losses")
        self.losses = self.get_value_from_config_file("total end stats","losses")
                
    def log_tie(self):
        self.add_one_to_value_from_config_file("total end stats","ties")     
        self.ties = self.get_value_from_config_file("total end stats","ties")
                
    def get_number_of_wins(self):
        if self.wins is None:
            return self.get_value_from_config_file("total end stats","wins")
        else:
            return self.wins
    def get_number_of_losses(self):
        if self.losses is None:
            return self.get_value_from_config_file("total end stats","losses")
        else:
            return self.losses

    def get_number_of_ties(self):
        if self.ties is None:
            return self.get_value_from_config_file("total end stats","ties")
        else:
            return self.ties

    def reset_stats(self):
        with open(self.path_config_file, 'w') as out_file:
            json.dump(self.initial_json_data, out_file, sort_keys = True, indent = 4, ensure_ascii = False)
        
        print("The stats of the model " + self.modelname + " have been reset")
    
    def reset_end_states(self):
        with open(self.path_config_file, 'r+') as file:
            json_data = json.load(file)
            list_categories=["total end stats","games end stats","training loops end stats"]
            list_items=["wins","losses","ties"]

            for category in list_categories:
                for item in list_items:
                    json_data[category][item] = 0

            file.seek(0)
            json.dump(json_data, file, sort_keys = True, indent = 4, ensure_ascii = False)
            print("updated values:",json_data)
            file.truncate()
        print("The end states of the model " + self.modelname + " have been reset")


