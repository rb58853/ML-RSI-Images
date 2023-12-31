from segmentation.sam import SAM
from features.features import ImageEmbedding#, ImageFeature
from PIL import Image
import cv2
import matplotlib.pyplot as plt

class ProcessImages:
    IMAGE_PARTITION = 80 #tamaño mínimo(en píxeles) de un cuadro de segmentación = tamaño(imagen)/IMAGE_PARTITION
    SEGMENTATION = 'box' #tipo de segmentacion a usar en sam

    def __init__(self) -> None:
        self.sam = SAM
        self.sam.import_model()
        self.AREA = 20*20
        self.Image = None
        self.image_features:list[ImageEmbedding] = []
    
    def get_images(self, image_path, segmentation = None):
        image = self.load_cv2_image(image_path)
        raw_image =self.load_pil_image(image_path)
        segm = ProcessImages.SEGMENTATION
        
        self.image_features = []
        self.image_features.append(ImageEmbedding(image, None))

        if segmentation is not None:
            segm = segmentation

        images = self.sam.all_areas_from_image(
            image= image, 
            raw_image = raw_image, 
            min_box_area = self.AREA, 
            min_area = self.AREA/2, 
            use_mask_as_return = segm == 'mask' or segm == 'full')[segm]
        
        for image in images:
            self.image_features.append(image)
        
        return self.image_features
    
    def get_segmentations(self, image_path):
        image = self.load_cv2_image(image_path)
        raw_image =self.load_pil_image(image_path)
        
        images = self.sam.all_areas_from_image(
            image= image, 
            raw_image = raw_image, 
            min_box_area = self.AREA, 
            min_area = self.AREA/2, 
            use_mask_as_return = True)
        return images

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
    
    def show_images(self, image_path = None, segmentation = None):
        segm = ProcessImages.SEGMENTATION
        if segmentation is not None:
            segm = segmentation
        
        if len(self.image_features) == 0:
            self.image_features = self.get_images(image_path, segmentation= segmentation)[segm]
        
        for image in self.image_features:
            plt.figure(figsize=(2,2))
            plt.title(f'{image}\npos: {image.position}\nsimilarity: {self.image_features.get_rank(image)}')
            plt.imshow(image.image)
            plt.axis('off')
            plt.show()