import torch
from PIL import Image
from scipy.spatial.distance import cosine
from transformers import CLIPProcessor, CLIPModel
from scipy.spatial import distance
import math

class ClipEmbedding:
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
        # return embedding
    
        #si quiere usarse numpy arrays cometar el return
        embedding_as_np = embedding.cpu().detach().numpy()
        return embedding_as_np
    
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
        # return text_embeds
    
        #si quiere usarse numpy arrays cometar el return
        embedding_as_np = text_embeds.cpu().detach().numpy()
        return embedding_as_np

    def process_text_and_get_pos(self, text):
        #procesar el texto y sacarle la posicion
        return None
    
    def get_text_vector(self, texts):
        embeddings = self.get_text_embedding(texts)
        return [(embedding, self.process_text_and_get_pos(text)) for embedding, text in zip(embeddings, texts)]

    def cosine_similarity(self, vec1, vec2):
        #En caso de volver a usar tensores en vez de numpys hay que descomentar
        vec1 = vec1#.cpu().detach().numpy()
        vec2 = vec2#.cpu().detach().numpy()
        return 1 - cosine(vec1, vec2)
    
    def euclidean_similarity(self, vec1, vec2):
        if vec1 is None or vec2 is None:
            return 0
        return math.sqrt(2) - distance.euclidean(vec1, vec2)
   
    def calculate_similarity(self, vec1, vec2):
        cosine_similarity = self.cosine_similarity(vec1[0], vec2[0])
        euclidean_similarity = self.euclidean_similarity(vec1[1], vec2[1])
        euclindean_umbral = pow(euclidean_similarity, ClipEmbedding.EUCLIDEAN_POW_UMBRAL)/ ClipEmbedding.EUCLIDEAN_DIV_UMBRAL
        
        return cosine_similarity * (1 + euclindean_umbral)