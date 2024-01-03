from environment.environment import is_installed_lib
from environment.environment import ImageEmbeddingEnv as env
from environment.environment import MatPlotLib as Color
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import math

from embedding.clip_embeding import ClipEmbedding
clip = ClipEmbedding()

if env.USE_CAPION_MODEL:
    env.CAPTION_MODEL.import_model()

class Feature:
    def __init__(self) -> None:
        self.items = []
        self.embedding = None
        self.position = None
        self.neighbords:dict[str:Text] = {
            'w':[],    
            'e':[],    
            'n':[],    
            's':[],    
            
            'nw':[],    
            'ne':[],    
            'sw':[],    
            'se':[],    
            
            'in':[],
            'beside':[],
            'next': [] #near. indica cercania tan solo sin posicion especifica    
        }
        self.caption = None
       
    def __getitem__(self, index):
       return self.items[index]
    
class ImageEmbedding(Feature):
    def __init__(self, image, position) -> None:
        super().__init__()
        self.image = image
        self.image_path = None
        
        self.id = 0
        self.name = 'image'
        self.embedding = None
        self.caption = None
        self.position = position
        
        self.multiple_captions = []
        
        self.left, self.right, self.top, self.buttom = (0,0,0,0)
        # self.neighbords = {
        #     'left':[],    
        #     'right':[],    
        #     'top':[],    
        #     'buttom':[],    
        #     'in':[],    
        # }
        
        self.items = [self.embedding, self.position, self.neighbords]
        
        self.similarity_with_origin = None

        if self.image is not None:
            self.get_embedding()
            self.get_caption()

    def get_caption(self):
        '''Genera un text como caption'''
        if self.image is None:
            raise Exception("Image is None")
        
        if env.USE_CAPION_MODEL:
            caption = Text(env.CAPTION_MODEL.caption(self.image), self.position)
            self.caption = caption

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
        if left: x = 'w'
        if right: x = 'e'
        if top: y = 'n'
        if buttom: y = 's'

        if x is not None:
            near = self.calculate_x_distance(x_dist, x_y_dist)
            if near > 0:
                self.neighbords[x].append((image, near))
                self.neighbords['beside'].append((image, near))
                self.neighbords['next'].append((image, near*0.9))
        if y is not None:
            near = self.calculate_y_distance(y_x_dist, y_dist)
            if near > 0:
                self.neighbords[y].append((image, near))
                self.neighbords['next'].append((image, near*0.9))
                # self.neighbords['beside'].append((image, near))

        if x is not None and y is not None:
            #Esto hay que mejorarlo. Multiplicar por angulo o algo. Queda decidir una metrica
            near = self.calculate_x_distance(x_dist, x_y_dist) + self.calculate_y_distance(y_x_dist, y_dist)
            self.neighbords[y+x].append((image, near))

        if in_x and in_y:
            self.neighbords['in'].append((image, env.max_similarity()))

    def set_neighbords(self, images_list):
        for key in self.neighbords:
            self.neighbords[key] = []
                    
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
        neighbords = {key: self.neight_to_list(key) for key in self.neighbords.keys()}
        return [
            self.embedding,
            self.position,
            neighbords
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
        return f'{self.name} {self.id}'
    
    def __repr__(self) -> str:
        return f'image {self.id}'

    def plot(self):
        if self.image is not None:
            plt.figure(figsize=(8,8))
            plt.title(f'{self} | pos: {self.position}')
            plt.imshow(self.image)
            plt.axis('off')
            plt.show()
        else:
            print("Image is None")    

class NeigbordsVariants(ImageEmbedding):         
    def angles_sim(self,image:ImageEmbedding):
        if image.position[0] > self.position[0]:
            if image.left > self.left:
                #estamos en presencia de un vecino derecho:
                x1,x2 = self.position[0],image.position[0]
                y1,y2 = self.position[1],image.position[1]
                y1,y2 = 1-y1,1-y2 #invertir eje y
               
                dx = x2 - x1
                dy = y2 - y1
                angle = math.atan2(dy, dx)
                sim_angle_right = angle/(math.pi*2)
                sim_angle_right = abs(sim_angle_right)
                sim_angle_right = 1/4-sim_angle_right #Calculos hechos
                sim_angle_right *= 4
                
                sim_angle_top_right = angle - math.pi/4
                sim_angle_top_right = abs(sim_angle_top_right)
                sim_angle_top_right /= (math.pi*2)
                sim_angle_top_right = 1/8 - sim_angle_top_right
                sim_angle_top_right *= 1/8 #Calculos hechos

                sim_angle_bottom_right = angle - (-math.pi/4)
                sim_angle_bottom_right = abs(sim_angle_bottom_right)
                sim_angle_bottom_right /= (math.pi*2)
                sim_angle_bottom_right = 1/8- sim_angle_bottom_right
                sim_angle_bottom_right *= 8

                x_dist = max(0,image.left - self.right)
                y_dist = 0
                if image.buttom < self.top:
                    #esta abajo
                    y_dist = max(self.top-image.buttom,0)
                    dist = math.sqrt(x_dist*x_dist + y_dist*y_dist) 
                    sim_dist = (env.MAX_DISTANCE-(dist))/env.POS_UMBRAL
                    if sim_dist > 0:
                        self.neighbords['e'].append((image, sim_dist * sim_angle_right))
                        self.neighbords['se'].append((image, sim_dist * sim_angle_bottom_right))

                elif image.top > self.buttom:
                    #esta arriba
                    y_dist = max(image.top-self.buttom,0)
                    dist = math.sqrt(x_dist*x_dist + y_dist*y_dist)
                    sim_dist = (env.MAX_DISTANCE-(dist))/env.POS_UMBRAL
                    if sim_dist > 0:
                        self.neighbords['e'].append((image, sim_dist * sim_angle_right))
                        self.neighbords['ne'].append((image, sim_dist * sim_angle_top_right))

                else:
                    #Esta contenido en el eje y  
                    dist = math.sqrt(x_dist*x_dist + y_dist*y_dist) 
                    sim_dist = (env.MAX_DISTANCE-(dist))/env.POS_UMBRAL
                    if sim_dist > 0:
                        self.neighbords['e'].append((image, sim_dist * sim_angle_right))
                        if image.position < self.position:
                            #esta arriba relativo al centro
                            self.neighbords['ne'].append((image, sim_dist * sim_angle_top_right))
                        if image.position > self.position:
                            #esta debajo relativo al centro
                            self.neighbords['se'].append((image, sim_dist * sim_angle_top_right))

        if image.position[0] < self.position[0]:
            if image.right < self.right:
                #estamos en presencia de un vecino izquierdo:
                x1,x2 = self.position[0],image.position[0]
                y1,y2 = self.position[1],image.position[1]
                y1,y2 = 1-y1,1-y2 #invertir eje y
                dx = x2 - x1
                dy = y2 - y1
                
                angle = math.atan2(dy, dx)
                if angle<0 : angle += 2*math.pi #hacerlo positivo

                sim_angle_left = angle - math.pi
                sim_angle_left = abs(sim_angle_left)
                sim_angle_left = sim_angle_left/(math.pi*2)
                sim_angle_left = 1/4-sim_angle_left #Calculos hechos
                sim_angle_left *= 4
                
                sim_angle_top_left = angle - 3*math.pi/4
                sim_angle_top_left = abs(sim_angle_top_left)
                sim_angle_top_left /= (math.pi*2)
                sim_angle_top_left = 1/8 - sim_angle_top_left
                sim_angle_top_left *= 1/8 #Calculos hechos

                sim_angle_bottom_left = angle - (5*math.pi/4)
                sim_angle_bottom_left = abs(sim_angle_bottom_left)
                sim_angle_bottom_left /= (math.pi*2)
                sim_angle_bottom_left = 1/8- sim_angle_bottom_left
                sim_angle_bottom_left *= 8

                x_dist = max(0,image.right - self.left)
                y_dist = 0
                if image.buttom < self.top:
                    #esta abajo
                    y_dist = max(self.top - image.buttom,0)
                    dist = math.sqrt(x_dist*x_dist + y_dist*y_dist) 
                    sim_dist = (env.MAX_DISTANCE-(dist))/env.POS_UMBRAL
                    if sim_dist > 0:
                        self.neighbords['w'].append((image, sim_dist * sim_angle_left))
                        self.neighbords['sw'].append((image, sim_dist * sim_angle_bottom_left))

                elif image.top > self.buttom:
                    #esta arriba
                    y_dist = max(image.top -self.buttom,0)
                    dist = math.sqrt(x_dist*x_dist + y_dist*y_dist) 
                    sim_dist = (env.MAX_DISTANCE-(dist))/env.POS_UMBRAL
                    if sim_dist > 0:
                        self.neighbords['w'].append((image, sim_dist * sim_angle_left))
                        self.neighbords['nw'].append((image, sim_dist * sim_angle_top_left))

                else:
                    #Esta contenido en el eje y  
                    dist = math.sqrt(x_dist*x_dist + y_dist*y_dist) 
                    sim_dist = (env.MAX_DISTANCE-(dist))/env.POS_UMBRAL
                    if sim_dist > 0:
                        self.neighbords['w'].append((image, sim_dist * sim_angle_left))
                        if image.position < self.position:
                            #esta arriba relativo al centro
                            self.neighbords['nw'].append((image, sim_dist * sim_angle_top_left))
                        if image.position > self.position:
                            #esta debajo relativo al centro
                            self.neighbords['sw'].append((image, sim_dist * sim_angle_top_left))
        
        if image.position[1] >self.position[1]:
            if image.top > self.top:
                #esta debajo     
                x1,x2 = self.position[0],image.position[0]
                y1,y2 = self.position[1],image.position[1]
                y1,y2 = 1-y1,1-y2 #invertir eje y

                dx = x2 - x1
                dy = y2 - y1
                angle = math.atan2(dy, dx)
                
                sim_angle_bottom = angle - (-3*math.pi/2)
                sim_angle_bottom = abs(sim_angle_bottom)
                sim_angle_bottom = sim_angle_bottom/(math.pi*2)
                sim_angle_bottom = 1/4-sim_angle_bottom #Calculos hechos
                sim_angle_bottom *= 4

                y_dist = max(0,image.top - self.buttom)
                x_dist = max((self.left - image.right, image.left - image.right),0)
                
                dist = math.sqrt(x_dist*x_dist + y_dist*y_dist) 
                sim_dist = (env.MAX_DISTANCE-(dist))/env.POS_UMBRAL
                if sim_dist > 0:
                    self.neighbords['s'].append((image, sim_dist * sim_angle_bottom))

        if image.position[1] < self.position[1]:
            if image.top < self.top:
                #esta arriba     
                x1,x2 = self.position[0],image.position[0]
                y1,y2 = self.position[1],image.position[1]
                y1,y2 = 1-y1,1-y2 #invertir eje y

                dx = x2 - x1
                dy = y2 - y1
                angle = math.atan2(dy, dx)
                
                sim_angle_top = angle - (math.pi/2)
                sim_angle_top = abs(sim_angle_top)
                sim_angle_top = sim_angle_top/(math.pi*2)
                sim_angle_top = 1/4-sim_angle_top #Calculos hechos
                sim_angle_top *= 4

                y_dist = max(0,self.top - image.buttom)
                x_dist = max((self.left - image.right, image.left - image.right),0)
                
                dist = math.sqrt(x_dist*x_dist + y_dist*y_dist) 
                sim_dist = (env.MAX_DISTANCE-(dist))/env.POS_UMBRAL
                if sim_dist > 0:
                    self.neighbords['s'].append((image, sim_dist * sim_angle_top))    
                        

        for neigh in self.neighbords['w']:
            self.neighbords['beside'].append((neigh[0],neigh[1]*0.9))
        for neigh in self.neighbords['e']:
            self.neighbords['beside'].append((neigh[0],neigh[1]*0.9))
        
        keys = ['e','w','s','n','ne','nw','se','sw']
        for key in keys:
            for neigh in self.neighbords[key]:
                self.neighbords['next'].append((neigh[0],neigh[1]*0.85))

class Text(Feature):
    def __init__(self, text, position = None) -> None:
        super().__init__()
        self.text = text
        self.embedding = None
        self.set_embedding() 
        self.position = position
        # self.neighbords:dict[str:Text] = {
        #     'left':[],    
        #     'right':[],    
        #     'top':[],    
        #     'buttom':[],    
        #     'in':[],
        #     'near': [] #nex to. indica cercania tan solo sin posicion especifica    
        # }

    def set_embedding(self):
        if clip.model is not None:
            self.embedding = clip.get_text_embedding(self.text)[0]
        else:
            print(f"Not use embeding in TEXT, missed GPU")
            
    def set_position(self):
        raise NotImplementedError()
    
    def set_neighbords(self):
        raise NotImplementedError()
    
    def add_neighbord(self, text, pos_label):
        #TODO es 1 hay que cambiarlo a dinamico
        if pos_label is not None:
            self.neighbords[pos_label].append((text, 1))

    
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
        return f'text: {self.text}\npos: {self.position}'
    
    def __repr__(self) -> str:
        return self.text