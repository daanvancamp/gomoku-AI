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
    def create_new_model(self, modelName):
        # Directory 
        directory = modelName
  
        # Parent Directory path 
        parent_dir = "data/models"
  
        # Path 
        path = os.path.join(parent_dir, directory) 
        
        if not os.path.isdir(path):
            os.mkdir(path) 
            
        print("Directory '% s' created" % path) 
    
        # copy the contents of the demo.py file to  a new file called demo1.py
        shutil.copyfile('./data/templatemodel/model.pth', path + "/model.pth")
        
        json_data = {'parameter': 10}

        with open(path + "/modelconfig.txt", 'w') as out_file:
            json.dump(json_data, out_file, sort_keys = True, indent = 4, ensure_ascii = False)
       
    def get_list_models(self):
        subfolders = [ f.path for f in os.scandir('data/models') if f.is_dir() ]
        return subfolders
    
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