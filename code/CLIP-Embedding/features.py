from enviroment import is_installed_lib

from enviroment import ImageEmbeddingEnv as env
from enviroment import MatPlotLib as Color
from matplotlib.patches import Rectangle

clip = None
if is_installed_lib('torch'):
    from clip_embeding import ClipEmbedding
    clip = ClipEmbedding()

class Feature:
    def __init__(self) -> None:
        self.items = []
        self.embedding = None
        self.position = None
       
    def __getitem__(self, index):
       return self.items[index]
    
class ImageEmbedding(Feature):
    def __init__(self, image, position) -> None:
        self.image = image
        self.image_path = None
        self.embedding = None
        self.caption_embedding = None
        self.position = position
        self.id = 0
        self.left, self.right, self.top, self.buttom = (0,0,0,0)
        self.neighbords = {
            'left':[],    
            'right':[],    
            'top':[],    
            'buttom':[],    
            'in':[],    
        }
        self.items = [self.embedding, self.position, self.neighbords]
        self.similarity_with_origin = None
        if self.image is not None:
            self.get_embedding()


    def __getitem__(self, index):
       return self.items[index]
    
    def get_embedding(self):
        '''Genera el embedding con un modelo, en este caso clip'''
        if self.image is None:
            raise Exception("Image is None")
        self.embedding = clip.get_image_embedding(self.image)[0]
        self.items[0] = self.embedding

    def set_embedding(self, embedding):
        '''Setea un embedding, se usa para extraer el feature desde una lista'''
        self.embedding = embedding
        self.items[0] = self.embedding

    def set_limits(self, limits):
        '''Set in order: left, rigth, top, buttom'''
        self.left, self.right, self.top, self.buttom = limits
    
    def set_id(self, index):
        self.id = index 

    def set_as_neigh(self, image):
        y_dist = 0
        x_dist = 0
        x_y_dist = 0 #distancia relativa a y para el eje x.
        y_x_dist = 0 #distancia relativa a x para el eje y. Por ejemplo si en el eje x se solapa la distancia para calcular buttom y top relativa a x es cero y no `abs`

        left, right, top, buttom, in_x, in_y = (False,False,False,False, False, False)
        
        if image.position[0]< self.position[0]:
            #On left of self
            if image.right <= self.right and image.left < self.left:
                left = True
                x_dist =  max(self.left - image.right, 0)

                y_x_out = abs(self.left - image.left) #lo que se sale por la parte izquierda
                y_x_slide = abs(self.right - image.right) #Desplazamiento 
                y_x_dist = min(y_x_slide, y_x_out) #Minimo entre lo que se dsplaza y lo que sale de los limites
                # y_x_dist = abs(self.right - image.right) #desplazamiento
            else:
                in_x = image.left >= self.left and image.right <= self.right 

        if image.position[0] > self.position[0]:
            #On right of self
            if image.left >= self.left and image.right > self.right:
                right = True
                x_dist =  max(image.left - self.right, 0)
                
                y_x_out = abs(image.right - self.right) #lo que se sale por la parte derecha
                y_x_slide = abs(image.left - self.left) #Desplazamiento 
                y_x_dist = min(y_x_slide, y_x_out) #Minimo entre lo que se dsplaza y lo que sale de los limites
            else:
                in_x = image.left >= self.left and image.right <= self.right    

        if image.position[1] < self.position[1]:
            #On top of self
            if image.top < self.top and image.buttom <= self.buttom:
                top = True
                y_dist =  max(self.top - image.buttom,0)
                
                x_y_out = abs(image.buttom - self.buttom)#Lo que se sale por debajo
                x_y_slide = abs(self.top - image.top) #Desplzamiento
                x_y_dist = min(x_y_out, x_y_slide) 
            else:
                in_y = image.top >= self.top and image.buttom <= self.buttom

        if image.position[1] > self.position[1]:
            #On buttom of self
            if image.buttom > self.buttom and image.top >= self.top:
                buttom = True
                y_dist =  max(image.top - self.buttom, 0)
      
                x_y_out = abs(image.buttom - self.buttom) #Lo que se sale por debajo
                x_y_slide = abs(self.top - image.top) #Desplzamiento
                x_y_dist = min(x_y_out, x_y_slide) 
            else:
                in_y = image.top >= self.top and image.buttom <= self.buttom
        
        x = None
        y = None
        if left: x = 'left'
        if right: x = 'right'
        if top: y = 'top'
        if buttom: y = 'buttom'

        if x is not None:
            near = self.calculate_x_distance(x_dist, x_y_dist)
            if near > 0:
                self.neighbords[x].append((image, near))
        if y is not None:
            near = self.calculate_y_distance(y_x_dist, y_dist)
            if near > 0:
                self.neighbords[y].append((image, near))

        if in_x and in_y:
            self.neighbords['in'].append((image, env.max_similarity()))

    def set_neighbords(self, images_list):
        for image in images_list:
            if image != self:
                self.set_as_neigh(image)

    def calculate_x_distance(self, x_dist, y_dist):
        #Definir la funcion como deb ser
        x = pow(x_dist,env.PRIMARY_POW)
        y = pow(y_dist,env.SECUNDARY_POW)
        if x+y >= env.MAX_DISTANCE:
            return -1
        return (env.MAX_DISTANCE-(x + y))/env.POS_UMBRAL

        return(x_dist, y_dist)

    def calculate_y_distance(self, x_dist, y_dist):
        #Definir la funcion como deb ser
        x = pow(x_dist,env.SECUNDARY_POW)
        y = pow(y_dist,env.PRIMARY_POW)
        if x+y >= env.MAX_DISTANCE:
            return -1
        return (env.MAX_DISTANCE-(x + y))/env.POS_UMBRAL
        
        return(x_dist, y_dist)
    
    def neight_to_list(self,key):
        return [(item[0].id, item[1]) for item in self.neighbords[key]]

    def to_list(self):
        return [
            self.embedding,
            self.position,
            (   #Neighbords
                self.neight_to_list('left'), 
                self.neight_to_list('right'), 
                self.neight_to_list('top'), 
                self.neight_to_list('buttom'), 
                self.neight_to_list('in') 
            ) 
        ]
    
    def info(self):
        return f'\
        {self}\n\
        pos: {self.position}\n\
        left: {self.left}\n\
        right: {self.right}\n\
        top: {self.top}\n\
        buttom: {self.buttom}\n\
        '
    
    def print_neighbords(self):
        print(f'\t___ {self} ___'.upper())
        for key, value in zip(self.neighbords.keys(), self.neighbords.values()):
            if len(self.neighbords[key]) > 0:
                print(f'{key}:')
            for neigh in value:
                print(f'    ⦿ {neigh}')
    
    def plot_region(self,ax):
        x1, y1 = self.left, self.buttom
        x2, y2 = self.right, self.top
        # Calcular la anchura y altura del rectángulo
        width = x2 - x1
        height = y2 - y1

        color = Color.get_color()
        ax.text(self.position[0], self.position[1], str(self.id), ha='center', va='center', color=color)
        # Añadir el rectángulo a los ejes
        ax.add_patch(Rectangle((x1, y1), width, height, fill=False, edgecolor=color))

    def __str__(self) -> str:
        return f'image {self.id}'
    
    def __repr__(self) -> str:
        return f'image {self.id}'

class Text:
    def __init__(self, text, position = None) -> None:
        self.text = text
        self.embedding = None
        if is_installed_lib('torch'):
            self.set_embedding() 
        self.position = position
        self.neighbords:dict[str:Text] = {
            'left':[],    
            'right':[],    
            'top':[],    
            'buttom':[],    
            'in':[],
            'near': [] #nex to. indica cercania tan solo sin posicion especifica    
        }

    def set_embedding(self):
        self.embedding = clip.get_text_embedding(self.text)[0]
    
    def set_position(self):
        raise NotImplementedError()
    
    def set_neighbords(self):
        raise NotImplementedError()
    
    def set_pos(self, pos):
        self.position = pos
    
    def print(self):
        print(f'text: {self.text}')
        print(f'pos: {self.position}')
        keys=['left','right','top','buttom','in','near']
        
        for key in keys:
            if len(self.neighbords[key]) > 0:
                print(f'{key}: ',end="")
                for item in self.neighbords[key]:
                    print(item, end=" | ")
                print('\n')

    def __str__(self) -> str:
        return f'text: {self.text}\n\
        pos: {self.position}'
    
    def __repr__(self) -> str:
        return self.text