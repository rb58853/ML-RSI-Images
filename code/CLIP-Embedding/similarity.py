from features import Feature, Text, ImageEmbedding
from scipy.spatial.distance import cosine
from scipy.spatial import distance
import math

EUCLIDEAN_POW_UMBRAL = 1 #Elevar a la potencia la distancia euclieana
EUCLIDEAN_DIV_UMBRAL = 10 #dividir la distancia euclideana.
MIN_SIMILARTY_FOR_REGIONS = 0.26 #Si la similitud es menor que esto se considera insignificante y se deja de usar
MIN_NICE_SIMILARITY = 0.22 #Esta es la similitud a partir de a cual puede considerarse util algo
USE_NEGATIVE_REGIONS = True #Define si las regiones pueden aportar efecto negativo a la similitud, en el caso de hablar de cercania entre un objeto y otro

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
        
        value = math.sqrt(2) - distance.euclidean(vec1.position, vec2.position) 
        value_umbral = pow(value, EUCLIDEAN_POW_UMBRAL)/ EUCLIDEAN_DIV_UMBRAL
        return value_umbral
   
    def cosine_and_pos(vec1:Feature, vec2:Feature):
        cosine_similarity = Similarity.cosine(vec1, vec2)
        euclidean_similarity = Similarity.euclidean(vec1, vec2)
        
        if cosine_similarity > MIN_NICE_SIMILARITY:
            #Si en la posicion dada esta algo parecido a lo esperado, mejora el resultado
            return cosine_similarity * (1 + euclidean_similarity)
        else:
            #Si en la posicion dada esta algo que no es lo esperado empeora el resultado
            return cosine_similarity * (1 - euclidean_similarity)

    def region(text:Text, image:ImageEmbedding, print_ = False):
        end_sim = 0
        for key in ['left','right', 'top', 'buttom','in']:
            end_sim_region = 0
            for temp_text in text.neighbords[key]:
                max_sim = 0
                if USE_NEGATIVE_REGIONS:
                    max_sim = -1

                if print_:
                    print(f'\nTEXT: {temp_text}')
                    print(f'images in {key} region:'.upper())


                for temp_image in image.neighbords[key]:
                    similarity = Similarity.cosine_and_pos(temp_text, temp_image[0])
                    # similarity = Similarity.calculate(temp_text, temp_image[0]) #Esto es mejor pero hay que controlar la recursividad infinita
                    sim_dist = temp_image[1] #esta es la similitud por distancia que hay desde la imagen hacia su vecino
                    if similarity > MIN_SIMILARTY_FOR_REGIONS:
                        sim_for_neigh = sim_dist * similarity
                        max_sim = max(sim_for_neigh, max_sim)
                    else:
                        if USE_NEGATIVE_REGIONS:
                            sim_for_neigh = sim_dist * (similarity - MIN_SIMILARTY_FOR_REGIONS)
                            max_sim = max(sim_for_neigh, max_sim)
                    if print_:
                        print(f'   ⦿ {temp_image[0]}: {similarity}')        
                
                if max_sim == -1:
                    max_sim = 0
                if print_:
                    print(f'max_similarity: {max_sim}')    
                end_sim_region += max_sim
            end_sim +=end_sim_region
            
            if print_:
                print(f'end_similarity: {end_sim}')    
            
        return end_sim        
 
    def calculate(text:Text, image:ImageEmbedding, print_ = False):
        sim = Similarity.cosine_and_pos(text, image)
        if sim > MIN_SIMILARTY_FOR_REGIONS:
            sim *= (1+Similarity.region(text,image,print_))
        return sim    