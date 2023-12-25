from features import Feature, Text, ImageEmbedding
from scipy.spatial.distance import cosine
from scipy.spatial import distance
import math

EUCLIDEAN_POW_UMBRAL = 1 #Elevar a la potencia la distancia euclieana
EUCLIDEAN_DIV_UMBRAL = 10 #dividir la distancia euclideana.
MIN_SIMILARTY_FOR_REGIONS = 0.2 #Si la similitud es menor que esto se considera insignificante y se deja de usar

class Similarity:
    def cosine(vec1:Feature, vec2:Feature):
        #En caso de volver a usar tensores en vez de numpys hay que descomentar
        vec1 = vec1.embedding #.cpu().detach().numpy()
        vec2 = vec2.embedding #.cpu().detach().numpy()
        return 1 - cosine(vec1, vec2)
    
    def euclidean(vec1:Feature, vec2:Feature):
        #calcula similitud por distancia euclineada
        if vec1.position is None or vec2.position is None:
            return 0
        return math.sqrt(2) - distance.euclidean(vec1.position, vec2.position)
   
    def cosine_and_pos(vec1:Feature, vec2:Feature):
        cosine_similarity = Similarity.cosine(vec1, vec2)
        euclidean_similarity = Similarity.euclidean(vec1, vec2)
        euclindean_umbral = pow(euclidean_similarity, EUCLIDEAN_POW_UMBRAL)/ EUCLIDEAN_DIV_UMBRAL
        
        return cosine_similarity * (1 + euclindean_umbral)

    def region(text:Text, image:ImageEmbedding):
        for key in ['left','right', 'top', 'buttom','in']:
            end_sim = 0
            for temp_text in text.neighbords[key]:
                max_sim = 0
                for temp_image in image.neighbords[key]:
                    similarity = Similarity.cosine_and_pos(temp_text, temp_image[0])
                    # similarity = Similarity.calculate(temp_text, temp_image[0]) #Esto es mejor pero hay que controlar la recursividad infinita
                    if similarity > MIN_SIMILARTY_FOR_REGIONS:
                        sim_dist = temp_image[1] #esta es la similitud por distancia que hay desde la imagen hacia su vecino
                        sim_for_neigh = sim_dist * similarity
                        max_sim = max(sim_for_neigh, max_sim)
                end_sim+=max_sim
 
    def calculate(text:Text, image:ImageEmbedding):
        sim = Similarity.cosine_and_pos(text, image)
        if sim > MIN_SIMILARTY_FOR_REGIONS:
            sim *= (1+Similarity.region(text,image))
        return sim    