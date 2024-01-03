from features.features import Feature, Text, ImageEmbedding
# from image_manager import ImageFeature
from features.text_manager import TextFeature
from environment.environment import ImageEmbeddingEnv as image_env
from scipy.spatial.distance import cosine
from scipy.spatial import distance
import math

EUCLIDEAN_POW_UMBRAL = 1 #Elevar a la potencia la distancia euclieana
EUCLIDEAN_DIV_UMBRAL = 10 #dividir la distancia euclideana.
MIN_SIMILARTY_FOR_REGIONS = 0.24 #Si la similitud es menor que esto se considera insignificante y se deja de usar
MIN_NICE_SIMILARITY = 0.24 #Esta es la similitud a partir de a cual puede considerarse util algo
MIN_NICE_SIMILARITY_ORIGIN = 0.22 #Esta es la similitud a partir de a cual puede considerarse util algo en la imagen original y texto original
MIN_NICE_USE_CAPTION_SIMILARITY = 0.65 #Esta es la similitud a partir de a cual puede considerarse util algo a nivel de texto contra texto
USE_NEGATIVE_REGIONS = True #Define si las regiones pueden aportar efecto negativo a la similitud, en el caso de hablar de cercania entre un objeto y otro
IMPORTANCE_NEGATIVE_REGIONS = 2 #Esto defne que tan importante es una region negativa, mientras mas alto, mas baja la similitud una region mala

if image_env.USE_CAPION_MODEL:
    MIN_NICE_SIMILARITY = (MIN_NICE_SIMILARITY + MIN_NICE_USE_CAPTION_SIMILARITY)/2
    MIN_NICE_SIMILARITY_ORIGIN = (MIN_NICE_SIMILARITY_ORIGIN + MIN_NICE_USE_CAPTION_SIMILARITY)/2

class Similarity:
    def cosine(vec1:Feature, vec2:ImageEmbedding):
        if vec2.caption is not None and image_env.USE_CAPION_MODEL:
            v1 = vec1.embedding
            v2 = vec2.embedding
            v3 = vec2.caption.embedding
            caption_sim = 1- cosine(v1, v3)
            image_sim = 1- cosine(v1, v2)

            if caption_sim < MIN_NICE_SIMILARITY:
                pow(caption_sim, image_env.CAPTION_IMPORTANCE) #si es malo amenta lo malo que eres
            else:
                pow(caption_sim, 1/image_env.CAPTION_IMPORTANCE) #si es bueno aumenta lo bueno que eres

            cos = (image_sim + caption_sim)/2
            return cos

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
   
    def cosine_and_pos(vec1:Text, vec2:ImageEmbedding):
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
        for key in Feature().neighbords.keys():
            end_sim_region = 0
            for temp_text in text.neighbords[key]:
                max_sim = 0
                if USE_NEGATIVE_REGIONS:
                    max_sim = -1

                if print_:
                    print(f'\nTEXT: {temp_text[0]}')
                    print(f'images in {key} region:'.upper())


                for temp_image in image.neighbords[key]:
                    # similarity = Similarity.cosine(temp_text, temp_image[0])
                    similarity = Similarity.cosine_and_pos(temp_text[0], temp_image[0])
                    # similarity = Similarity.calculate(temp_text, temp_image[0]) #Esto es mejor pero hay que controlar la recursividad infinita
                    sim_dist = temp_image[1] #esta es la similitud por distancia que hay desde la imagen hacia su vecino
                    if similarity > MIN_SIMILARTY_FOR_REGIONS:
                        sim_for_neigh = sim_dist * similarity
                        max_sim = max(sim_for_neigh, max_sim)
                    else:
                        if USE_NEGATIVE_REGIONS:
                            sim_for_neigh = sim_dist * (pow(similarity,IMPORTANCE_NEGATIVE_REGIONS) - MIN_SIMILARTY_FOR_REGIONS)
                            max_sim = max(sim_for_neigh, max_sim)
                    if print_:
                        try:print(f'   ⦿ {temp_image[0]}: {sim_for_neigh}')        
                        except:pass
                        
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

    # def full(texts:TextFeature, images: ImageFeature):
    def full(texts:TextFeature, images):
        origin_sim = Similarity.cosine(texts.origin, images.origin)
        acumulate = 0
        for text in texts:
            if text.position is None:
                if not True in [ item != [] for item in text.neighbords.values()]:
                    #Si todos los vecinos son vacios y no se indica posicion, entonces no buscar similitud
                    continue
            sim_for_text = 0
            im = None
            for image in images:
                if image != images.origin:
                    sim_region = Similarity.calculate(text,image, False)
                    if sim_region <= Similarity.cosine_and_pos(text,image) and text.position is None:
                        continue

                    # sim_region = Similarity.calculate(text,image, True)
                    if sim_region > MIN_NICE_SIMILARITY:
                        sim_for_text = max(sim_for_text, sim_region)
                        if sim_region > sim_for_text:
                            im = image
                            
            acumulate += sim_for_text        

        if origin_sim > MIN_NICE_SIMILARITY:
            return acumulate + origin_sim
        
        return max(acumulate, origin_sim)    
  
