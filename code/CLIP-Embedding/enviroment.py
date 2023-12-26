import importlib

def is_installed_lib(name):
   try:
       importlib.import_module(name)
       return True
   except ImportError:
       return False
   
class ImageEmbeddingEnv:
    ''' 
    ## ImageEmbeddingEnv
    ### Variables 
    - `POS_UMBRAL`: Importancia dada a la distancia entre las posiciones de las imagenes, mientras menor valor mayor importancia se le da a las posiciones
    - `PRIMARY_POW`: Elevacion a la ptencia del eje principal a la hora de calcular distancias
    - `SECUNDARY_POW`: Elevacion a la ptencia del eje no principal a la hora de calcular distancias
    - `MAX_DISTANCE`: Distancia maxima que puede haber entre dos imagenes para ser consideradas vecinas
    ### Funciones
    - `max_similarity()`: Devuelve la maxima similitud que se puede alcanzar en la distancia entre dos imagenes. 
    '''
    PRIMARY_POW = 1 #Elevacion a la ptencia del eje principal a la hora de calcular distancias
    SECUNDARY_POW = 0.5 #Elevacion a la ptencia del eje no principal a la hora de calcular distancias
    MAX_DISTANCE = 1 #Distancia maxima que puede haber entre dos imagenes para ser consideradas vecinas
    POS_UMBRAL = 1

    def max_similarity():
        return ImageEmbeddingEnv.MAX_DISTANCE/ImageEmbeddingEnv.POS_UMBRAL

class MatPlotLib:
    INDEX = -1
    COLORS = [ 'black', 'blue', 'red', 'green', 'blueviolet', 'cornflowerblue', 'darkblue', 'darkcyan', 'darkgreen', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkred', 'darkseagreen', 'darkslateblue', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dodgerblue','forestgreen', 'fuchsia', 'green', 'greenyellow', 'hotpink', 'indianred', 'indigo', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightgreen', 'lime', 'limegreen', 'magenta', 'mediumaquamarine', 'mediumblue', 'mediumpurple', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'palegreen', 'paleturquoise','pink', 'purple', 'royalblue', 'skyblue', 'slateblue', 'tomato', 'turquoise', 'violet']
    
    def get_color():
        MatPlotLib.INDEX = (1+MatPlotLib.INDEX) % len(MatPlotLib.COLORS)

        return MatPlotLib.COLORS[MatPlotLib.INDEX]

class SamEnv:
    '''
    -  `points_per_side` define el número de puntos que se utilizan para generar las máscaras. Reducir este número puede acelerar el proceso de segmentación, pero también podría resultar en máscaras menos precisas.
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