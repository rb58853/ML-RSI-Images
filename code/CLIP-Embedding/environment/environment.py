import importlib
import sys

def is_installed_lib(name):
   try:
       importlib.import_module(name)
       return True
   except ImportError:
       return False
   
class Colab:
    RUN_ONLY_IN_COLAB = True
    def use_in_local():
        if not Colab.RUN_ONLY_IN_COLAB:
            return True
        return 'google.colab' in sys.modules
   
class ImageEmbeddingEnv:
    ''' 
    ## ImageEmbeddingEnv
    ### Variables 
    - `USE_MULTIPLE_CAPIONS` Si esto esta activo se hara una subdivision de los captions y se buscara similitud todos contra todos(menos eficiente)
    - `USE_CAPION_MODEL` Indica que se usara un modelo de descripciones de imagenes para usar tambien emedding de la descrpcion en la imagen al calcular similitud
    - `CAPTION_MODEL` Este es el modelo que se usara para describir la imagen
    - `CAPTION_IMPORTANCE` Importancia del caption, define que tan importante sera el caption de una imagen para la similitud. `=1` indica que tiene igual imporatancia que la imagen
    - `POS_UMBRAL`: Importancia dada a la distancia entre las posiciones de las imagenes, mientras menor valor mayor importancia se le da a las posiciones
    - `PRIMARY_POW`: Elevacion a la ptencia del eje principal a la hora de calcular distancias
    - `SECUNDARY_POW`: Elevacion a la ptencia del eje no principal a la hora de calcular distancias
    - `MAX_DISTANCE`: Distancia maxima que puede haber entre dos imagenes para ser consideradas vecinas
    - `KEY_IMAGES`: Esto es el tipo de imagen que usara como principal. (box or mask).
    ### Funciones
    - `max_similarity()`: Devuelve la maxima similitud que se puede alcanzar en la distancia entre dos imagenes. 
    '''
    from caption_models.blip2 import BLIP2
    from caption_models.blip import BLIP
    
    USE_MULTIPLE_CAPIONS = False
    USE_CAPION_MODEL = False
    CAPTION_MODEL =BLIP
    CAPTION_IMPORTANCE = 1

    PRIMARY_POW = 1.2 #Elevacion a la ptencia del eje principal a la hora de calcular distancias
    SECUNDARY_POW = 0.7 #Elevacion a la ptencia del eje no principal a la hora de calcular distancias
    MAX_DISTANCE = 1 #Distancia maxima que puede haber entre dos imagenes para ser consideradas vecinas
    POS_UMBRAL = 0.85

    KEY_IMAGES = 'box'

    def max_similarity():
        return ImageEmbeddingEnv.MAX_DISTANCE/ImageEmbeddingEnv.POS_UMBRAL

class MatPlotLib:
    INDEX = -1
    COLORS = [ 'black', 'blue', 'red', 'green', 'blueviolet', 'cornflowerblue', 'darkblue', 'darkcyan', 'darkgreen', 'darkkhaki', 'darkmagenta', 'darkorange', 'darkred', 'darkseagreen', 'darkslateblue', 'darkturquoise', 'darkviolet', 'green', 'magenta','pink', 'purple', 'royalblue', 'slateblue', 'tomato', 'turquoise', 'violet']
    
    def get_color():
        MatPlotLib.INDEX = (1+MatPlotLib.INDEX) % len(MatPlotLib.COLORS)

        return MatPlotLib.COLORS[MatPlotLib.INDEX]

class SamEnv:
    '''
    - `points_per_side` define el número de puntos que se utilizan para generar las máscaras. Reducir este número puede acelerar el proceso de segmentación, pero también podría resultar en máscaras menos precisas.
    - `pred_iou_thresh` define el umbral para la intersección sobre la unión (IOU) en las predicciones. Aumentar este valor puede resultar en menos regiones propuestas, acelerando el proceso de segmentación.
    - Aumentar `stability_score_thresh` puede resultar en menos regiones propuestas.
    - `crop_n_layers` define el número de capas en el recorte de la imagen. Reducir este número puede acelerar el proceso de segmentación, pero podría afectar negativamente la precisión del modelo.
    - Aumentar `crop_n_points_downscale_factor` puede resultar en menos puntos en el recorte de la imagen, acelerando el proceso de segmentación.
    - Aumentar el área mínima de la región de la máscara: Aumentar min_mask_region_area puede resultar en menos regiones propuestas, acelerando el proceso de segmentación.
    '''
    
    points_per_side=32
    pred_iou_thresh=0.86
    stability_score_thresh=0.92
    crop_n_layers=1
    crop_n_points_downscale_factor=2
    min_mask_region_area= 20*20

from environment.relevance_env import DistanteTextsRelevace #use as import
