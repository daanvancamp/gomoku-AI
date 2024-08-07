import os
import shutil
import json

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
    def get_total_number_of_training_loops(self,modelname):
        try:
            if os.path.exists("data/models/" + modelname + "/modelconfig.json"):
                with open("data/models/" + modelname + "/modelconfig.json", "r") as file:
                    data = json.load(file)
                    return data["training loops"]
            else:
                return 0
        except PermissionError:
            print("Please close the file and try again")
    def log_number_of_training_loops(self, modelname,number_of_additional_training_loops,opponent):
        print("log tr loops...")
        if os.path.exists("data/models/" + modelname + "/modelconfig.json"):
            with open("data/models/" + modelname + "/modelconfig.json", "r") as file:
                data = json.load(file)
                data["training loops"] += number_of_additional_training_loops
                data["training loops against "+opponent] += number_of_additional_training_loops
                with open("data/models/" + modelname + "/modelconfig.json", "w") as file:
                    json.dump(data, file, sort_keys = True, indent = 4, ensure_ascii = False)
        else:
            raise Exception("Config file not found, try to delete the model and create it again")
            with open("data/models/" + modelname + "/modelconfig.json", "w") as file:
                data ={"training loops": number_of_additional_training_loops,
                       "training loops against "+opponent: number_of_additional_training_loops
                       }
                json.dump(data, file, sort_keys = True, indent = 4, ensure_ascii = False)

    def create_new_model(self, modelName):
        # Directory 
        directory = modelName
  
        # Parent Directory path 
        parent_dir = "data/models"
  
        # Path 
        path = os.path.join(parent_dir, directory) 
        
        if not os.path.isdir(path):
            os.mkdir(path)
            
        if not directory=="" and directory is not None:
            if not os.path.exists(path):
                print("Directory '% s' created" % path) 
            else:
                print("Directory already existed, please give a unique name")
        else:
            print("Directory '% s' not created" % path,"please specify a valid name instead of an empty string")
        
        shutil.copyfile('./data/templatemodel/model.pth', path + "/model.pth")
        
        json_data = {'training loops': 0,
                     "training loops against Human": 0,
                     "training loops against AI-Model": 0,
                     "training loops against Test Algorithm": 0
                     }

        with open(path + "/modelconfig.json", 'w') as out_file:
            json.dump(json_data, out_file, sort_keys = True, indent = 4, ensure_ascii = False)
       
    def get_list_models(self):
        subfolders = [ f.path for f in os.scandir('data/models') if f.is_dir() ]
        models = []
        for folder in subfolders:
            # Adding an integer to the list
            models.append(folder.split('\\')[-1])        
        return models

    def delete_model(self, modelName):
        # Parent Directory path 
        parent_dir = "data/models"
        # Path 
        path = os.path.join(parent_dir, modelName) 
        shutil.rmtree(path)
        
        print("Directory '% s' deleted" % path) 


if __name__ == "__main__":
    # The client code.
    mm = ModelManager()
    mm.create_new_model("wim")
    #mm.delete_model("wim")