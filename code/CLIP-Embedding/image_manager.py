import matplotlib.pyplot as plt
from features import ImageEmbedding

class ImageFeature:
    def __init__(self) -> None:
        self.images:list[ImageEmbedding] = []
        self.ranking:dict[ImageEmbedding:float] = {}

    def get_rank(self, image:ImageEmbedding):
        try:
            return self.ranking[image]
        except:
            return None
        
    def from_list(self, list_images):
        self.images = []

        for feature in list_images:
            image = ImageEmbedding(None, feature[1])    
            image.set_embedding(feature[0])
            image.set_id(self.__len__())
            self.images.append(image)
        
        for i, feature in zip(range(self.__len__()),list_images):
            image = self.images[i]
            for neigh in feature[2][0]: image.neighbords['left'].append(self.convert_to_neighbord(neigh))
            for neigh in feature[2][1]: image.neighbords['right'].append(self.convert_to_neighbord(neigh))
            for neigh in feature[2][2]: image.neighbords['top'].append(self.convert_to_neighbord(neigh))
            for neigh in feature[2][3]: image.neighbords['buttom'].append(self.convert_to_neighbord(neigh))
            for neigh in feature[2][4]: image.neighbords['in'].append(self.convert_to_neighbord(neigh))

    def clear(self):
        self.images = []

    def to_list(self):
        return [image.to_list() for image in self.images]
    
    def add_image(self, image:ImageEmbedding):
        image.set_id(self.__len__())
        self.images.append(image)

    def get_image_from_id(self, id):
        return self.images[id]
    
    def convert_to_neighbord(self, neigh):
        return (self.get_image_from_id(neigh[0]), neigh[1])
    
    def __len__(self):
        return len(self.images)
    
    def set_neighbords(self):
        segms = [image for image in self.images if image != self.images[0]]#No usar la imagen original
        for image in segms:
                image.set_neighbords(segms)

    def __getitem__(self, index)-> ImageEmbedding:
       return self.images[index]
    
    def plot_regions(self):
        fig, ax = plt.subplots()
        ax.invert_yaxis()
        # Mostrar la imagen en los ejes con origin='lower'
        if self.images[0].image is not None:
            ax.imshow(self.images[0].image, extent=[0, 1, 1, 0], alpha=0.5)
        
        for image in self.images:
            if image == self.images[0]:continue #la primera imagen es la original
            image.plot_region(ax)
        plt.show()

    def set_ranking(self, ranking):
        self.ranking = ranking

class ImagesDataset:
    def __init__(self) -> None:
        self.features:list[ImageFeature] =[]
        pass

    def save_to_path(file):
        pass

    def load_from_path(file):
        pass