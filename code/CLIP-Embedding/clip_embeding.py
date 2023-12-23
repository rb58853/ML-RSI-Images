import torch
from PIL import Image
from scipy.spatial.distance import cosine
from transformers import CLIPProcessor, CLIPModel
from sam import SAM
import cv2
import matplotlib.pyplot as plt
from scipy.spatial import distance

class ClipEmbedding():
    EUCLIDEAN_POW_UMBRAL = 1 #Elevar a la potencia la distancia euclieana
    EUCLIDEAN_DIV_UMBRAL = 10 #dividir la distancia euclideana.

    def __init__(self) -> None:
        self.model, self.processor, self.device = self.get_model()
        
    def get_model(self):    
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        model = model.to(device)
        return(model, processor, device)

    def get_image_embedding(self, image):
        image_process = self.processor(
           text=None,
           images=image,
           return_tensors="pt"
        )["pixel_values"].to(self.device)

        embedding = self.model.get_image_features(image_process)
        return embedding
    
        # embedding_as_np = embedding.cpu().detach().numpy()
        # return embedding_as_np
    
    def get_text_embedding(self,text):
        image =  Image.new('RGB', (10, 10), color = (0, 0, 0))
        if not isinstance(text, list):
            text = [text]
        encoded_text = self.processor(
            text = text,
            images = image,
            padding=True,
            # truncation=True,
            # max_length=100,
            return_tensors='pt').to(self.device)

        outputs = self.model(**encoded_text)
        text_embeds = outputs['text_embeds']
        return text_embeds

    def process_text_and_get_pos(self, text):
        #procesar el texto y sacarle la posicion
        return None
    
    def get_text_vector(self, texts):
        embeddings = self.get_text_embedding(texts)
        return [(embedding, self.process_text_and_get_pos(text)) for embedding, text in zip(embeddings, texts)]

    def cosine_similarity(self, vec1, vec2):
        vec1 = vec1.cpu().detach().numpy()
        vec2 = vec2.cpu().detach().numpy()
        return 1 - cosine(vec1, vec2)
    
    def euclidean_similarity(self, vec1, vec2):
        if vec1 is None or vec2 is None:
            return 0
        return 1 - distance.euclidean(vec1, vec2)
   
    def calculate_similarity(self, vec1, vec2):
        cosine_similarity = self.cosine_similarity(vec1[0], vec2[0])
        euclidean_similarity = self.euclidean_similarity(vec1[1], vec2[1])
        euclindean_umbral = pow(euclidean_similarity, ClipEmbedding.EUCLIDEAN_POW_UMBRAL)/ ClipEmbedding.EUCLIDEAN_DIV_UMBRAL
        
        return cosine_similarity * (1 + euclindean_umbral) 

class ProcessImages:
    IMAGE_PARTITION = 80 #tamaño mínimo(en píxeles) de un cuadro de segmentación = tamaño(imagen)/IMAGE_PARTITION
    SEGMENTATION = 'box' #tipo de segmentacion a usar en sam

    def __init__(self) -> None:
        self.clip = ClipEmbedding()
        self.sam = SAM
        self.sam.import_model()
        self.AREA = 20*20
        self.segmentations = []

    def get_segmentation_images(self, image_path, segmentation = None):
        self.segmentations = []
        image = self.load_cv2_image(image_path)
        raw_image =self.load_pil_image(image_path)
        segm = ProcessImages.SEGMENTATION
        if segmentation is not None:
            segm = segmentation

        self.segmentations = self.sam.all_areas_from_image(
            image= image, 
            raw_image = raw_image, 
            min_box_area = self.AREA, 
            min_area = self.AREA/2, 
            use_mask_as_return = segm == 'mask' or segm == 'full')
        
        return {'images': self.segmentations[segm], 
                'pos': self.segmentations[f'{segm}_pos']}

    def get_embedding_segmentations(self, image_path, segmentation = None):
        segmentations = self.get_segmentation_images(image_path, segmentation = segmentation)
        embeddings = self.clip.get_image_embedding(segmentations['images'])
        positions = segmentations['pos']

        return [(embedding, pos) for embedding, pos in zip(embeddings, positions)]
        # return [self.clip.get_image_embedding(image) for image in self.segmentations]
    
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
        embeddings = self.get_embedding_segmentations(image_path, segmentation)
        
        image = self.load_pil_image(image_path)
        image_embedding = self.clip.get_image_embedding(image)
        image_embedding = (image_embedding[0], None)

        result = {}
        indexs = {}
        index = 0

        for embedding in embeddings:
            similarity = self.clip.calculate_similarity(embedding, image_embedding[0])
            result[similarity] = embedding
            indexs[similarity] = index
            index +=1

        result = dict(sorted(result.items(),reverse=True))
        
        if print_:
            for key in result:
                print(f'index_{indexs[key]}: {key}')
        
        return result
    
    def show_images(self, image_path = None, segmentation = None):
        if len(self.segmentations) == 0:
            self.segmentations = self.get_segmentation_images(image_path, segmentation= segmentation)
        
        segm = ProcessImages.SEGMENTATION
        if segmentation is not None:
            segm = segmentation

        index = 0
        for im in self.segmentations[segm]:
            plt.figure(figsize=(2,2))
            plt.title(f'index_{index} | pos: {self.segmentations[f"{segm}_pos"][index]}')
            plt.imshow(im)
            plt.axis('off')
            plt.show()
            index+=1
