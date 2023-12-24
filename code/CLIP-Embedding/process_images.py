import torch
from PIL import Image
from scipy.spatial.distance import cosine
from transformers import CLIPProcessor, CLIPModel
from sam import SAM
import cv2
import matplotlib.pyplot as plt
from scipy.spatial import distance
from image_embedding import ImageEmbedding, ImageFeature, clip
from clip_embeding import ClipEmbedding

class ProcessImages:
    IMAGE_PARTITION = 80 #tamaño mínimo(en píxeles) de un cuadro de segmentación = tamaño(imagen)/IMAGE_PARTITION
    SEGMENTATION = 'box' #tipo de segmentacion a usar en sam

    def __init__(self) -> None:
        self.sam = SAM
        self.sam.import_model()
        self.AREA = 20*20
        self.Image = None
        self.image_features:ImageFeature = ImageFeature()
    
    def set_neighbords(self):
        self.image_features.set_neighbords()

    def get_images(self, image_path, segmentation = None):
        image = self.load_cv2_image(image_path)
        raw_image =self.load_pil_image(image_path)
        segm = ProcessImages.SEGMENTATION
        
        self.image_features.clear()
        self.image_features.add_image(ImageEmbedding(image, (0.5,0.5)))

        if segmentation is not None:
            segm = segmentation

        self.image_features.images += self.sam.all_areas_from_image(
            image= image, 
            raw_image = raw_image, 
            min_box_area = self.AREA, 
            min_area = self.AREA/2, 
            use_mask_as_return = segm == 'mask' or segm == 'full')[segm]
        
        return self.image_features

    def load_pil_image(self,image_path):
        image = Image.open(image_path).convert("RGB")
        weigth, heigth = image.size
        self.AREA = (weigth * heigth)/ProcessImages.IMAGE_PARTITION
        return image
        
    def load_cv2_image(self,image_path):
        self.load_pil_image(image_path)
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image
    
    def ranking(self, image_path, segmentation = None, print_ = True):
        images = self.get_images(image_path, segmentation)
        
        image_origin = self.image_features[0]
        
        result = {}
        for image in images:
            similarity = clip.calculate_similarity(image, image_origin)
            result[similarity] = image

        result = dict(sorted(result.items(),reverse=True))
        end= {value: key for key,value in zip(result.keys(), result.values())}
        self.image_features.set_ranking(end)
        return end
    
    def show_images(self, image_path = None, segmentation = None):
        segm = ProcessImages.SEGMENTATION
        if segmentation is not None:
            segm = segmentation
        
        if len(self.image_features) == 0:
            self.image_features = self.get_images(image_path, segmentation= segmentation)[segmentation]
        
        for image in self.image_features:
            plt.figure(figsize=(2,2))
            plt.title(f'{image}-{image.position}')
            plt.imshow(image.image)
            plt.axis('off')
            plt.show()