from features.image_manager import ImageFeature
import json
import os

class ImagesDataset:
    def __init__(self) -> None:
        self.features:list[ImageFeature] =[]
        self.names:list[ImageFeature] =[]

    def save_to_path(self,path = './images/data'):
        for feature in self.features:
            imageSet = feature

            name = imageSet.path
            for i in range(len(name)-1,0,-1):
                if name[i] =='.':
                    name = name[:i]+'.json'
                    break
            name = name.split(os.path.sep)[-1]
            file_path = os.path.join(path, name) 
            with open(file_path , 'w') as json_file:
                json.dump(imageSet.to_list(), json_file)

    def load_from_dataset_path(self,path = './images/data'):
        files =  [file for file in os.listdir(path) if file.lower().endswith(('.json'))]
        files = [os.path.join(path, file) for file in files]
        
        for file in files:
            with open(file, 'r') as json_file:
                load_date = json.load(json_file)
        
            imageSet = ImageFeature()
            imageSet.from_list(load_date)
            self.append_image_set(imageSet)        

    def load_from_images_path(self,path, print_files = False):
        files =  [file for file in os.listdir(path) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
        files = [os.path.join(path, file) for file in files]
        
        if print_files:
            for file in files:
                print(file)

        for file in files:
            self.append(file)

    def append(self, path_image):
        name = path_image.split(os.path.sep)[-1] 
        if name in self.names:
            name +='_0'
        i = 1
        while name in self.names:
            name = name[0:-2]+ f'_{i}'
            i+=1
        self.names += name
        self.features.append(ImageFeature(path_image,name))

    def remove(self, item):
        if isinstance(item,str):
            #se asume que esta pasandole el name
            if item in self.names:
                index = self.names.index(item)
                self.features.remove(self.features[index])
        else:
            #se le pasa la imagen
            self.features.remove(item)
    
    def append_image_set(self, item):
        self.features.append(item)

    def __add__(self, other):
       result = ImagesDataset()
       result.features = self.features + other.features
       return result

    def __len__(self):
        return len(self.features)
    
    def __getitem__(self, index)-> ImageFeature:
       return self.features[index]
    
  