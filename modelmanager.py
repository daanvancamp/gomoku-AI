import os
import shutil
import json
import gomoku
class ModelManagerMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ModelManager(metaclass=ModelManagerMeta):
    def __init__(self):
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
            raise Exception("Config file not found, try to delete the model and create it again or replace the config file with the template file")
    
    def log_win(self, modelname):
        if os.path.exists("data/models/" + modelname + self.name_config_file):
            with open("data/models/" + modelname + self.name_config_file, "r") as file:
                data = json.load(file)
                data["wins"] += 1
                with open("data/models/" + modelname + self.name_config_file, "w") as file:
                    json.dump(data, file, sort_keys = True, indent = 4, ensure_ascii = False)
        else:
            raise Exception("Config file not found, try to delete the model and create it again or replace the config file with the template file")
    def log_loss(self, modelname):
        if os.path.exists("data/models/" + modelname + self.name_config_file):
            with open("data/models/" + modelname + self.name_config_file, "r") as file:
                data = json.load(file)
                data["losses"] += 1
                with open("data/models/" + modelname + self.name_config_file, "w") as file:
                    json.dump(data, file, sort_keys = True, indent = 4, ensure_ascii = False)
        else:
            raise Exception("Config file not found, try to delete the model and create it again or replace the config file with the template file")

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
                raise Exception("Config file not found, try to delete the model and create it again or replace the config file with the template file")

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

    def create_new_model(self, modelName):
        # Directory 
        directory = modelName
  
        # Path 
        path = os.path.join(self.parent_dir, directory) 
        
        if not os.path.isdir(path):
            os.mkdir(path)
            
        if not directory=="" and directory is not None:
            if not os.path.exists(path):
                print("Directory '% s' created" % path) 
            else:
                print("Directory already exists, please use a unique name")
        else:
            print("Directory '% s' not created" % path,"please specify a valid name instead of an empty string")
        
        shutil.copyfile('./data/templatemodel/model.pth', path + "/model.pth")
        
        
        with open(path + self.name_config_file, 'w') as out_file:
            json.dump(self.initial_json_data, out_file, sort_keys = True, indent = 4, ensure_ascii = False)
       
    def get_list_models(self):
        subfolders = [ f.path for f in os.scandir('data/models') if f.is_dir() ]
        models = []
        for folder in subfolders:
            # Adding an integer to the list
            models.append(folder.split('\\')[-1])
        return models

    def delete_model(self, modelName):
        # Path 
        path = os.path.join(self.parent_dir, modelName) 
        shutil.rmtree(path)
        
        print("Directory '% s' deleted" % path) 
    
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