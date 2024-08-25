import os
import shutil
from model_management.AI_model import AI_Model
from utils.singleton_class import Singleton


class ModelManager(metaclass=Singleton):
    def __init__(self):
        self.parent_dir = "data/models"
        self.list_models=self.get_list_models()

    def create_new_model(self, modelName:str):
        directory = modelName

        path = os.path.join(self.parent_dir, directory) 
        
        if not os.path.isdir(path):
            os.mkdir(path)
            
        if not directory=="" and directory is not None:
            print("Directory '% s' created" % path)

        else:
            print("Directory '% s' not created" % path,"please specify a valid name instead of an empty string")
        
        shutil.copyfile('./data/templatemodel/model.pth', path + "/model.pth")
        
        self.get_model(modelName).reset_stats(False)
       
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