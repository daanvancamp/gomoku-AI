import os
import shutil
import json
from AI_Model import AI_Model

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
    
    def get_model(self, modelName):
        return AI_Model(modelName)