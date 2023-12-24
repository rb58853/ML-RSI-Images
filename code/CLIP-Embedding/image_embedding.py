import math

class ImageEmbedding:
    def __init__(self, image, position) -> None:
        self.image = image
        self.embledding = None
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

    def set_embedding(self, embedding):
        self.embledding = embedding

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
                # x_dist =  abs(self.left - image.right)
                y_x_dist = abs(self.left - image.left) #lo que se sale por la parte izquierda
                # y_x_dist = abs(self.right - image.right)
            else:
                in_x = image.left >= self.left and image.right <= self.right 

        if image.position[0] > self.position[0]:
            #On right of self
            if image.left >= self.left and image.right > self.right:
                right = True
                x_dist =  max(image.left - self.right, 0)
                # x_dist =  abs(self.right - image.left)
                y_x_dist = abs(image.right - self.right) #lo que se sale por la parte derecha
                # y_x_dist = abs(image.left - self.left) #left de el menos el left mio
            else:
                in_x = image.left >= self.left and image.right <= self.right    

        if image.position[1] < self.position[1]:
            #On top of self
            if image.top < self.top and image.buttom <= self.buttom:
                top = True

                y_dist =  max(self.top - image.buttom,0)
                # y_dist =  abs(self.top - image.buttom)
                x_y_dist = abs(image.buttom - self.buttom)# + abs(self.top - image.top) #Lo que se sale por debajo + lo que falta por arriba
                # x_y_dist = abs(self.buttom - image.buttom) #El limite bajo mio - limite bajo de el
            else:
                in_y = image.top >= self.top and image.buttom <= self.buttom

        if image.position[1] > self.position[1]:
            #On buttom of self
            if image.buttom > self.buttom and image.top >= self.top:
                buttom = True
                y_dist =  max(image.top - self.buttom, 0)
                x_y_dist = abs(self.top - image.top)# + abs(image.buttom - self.buttom) #lo que se sale por encima + lo que falta por debajo
                # y_dist =  abs(self.buttom - image.top)
                # x_y_dist = abs(self.top - image.top)
            else:
                in_y = image.top >= self.top and image.buttom <= self.buttom
        
        x = None
        y = None
        if left: x = 'left'
        if right: x = 'right'
        if top: y = 'top'
        if buttom: y = 'buttom'

        if x is not None:
            self.neighbords[x].append((image, self.calculate_x_distance(x_dist, x_y_dist)))
        if y is not None:
            self.neighbords[y].append((image, self.calculate_y_distance(y_x_dist, y_dist)))
        
        if in_x and in_y:
            self.neighbords['in'] = (image, 0)

    def set_neighbords(self, images_list):
        for image in images_list:
            if image != self:
                self.set_as_neigh(image)

    def calculate_x_distance(self, x_dist, y_dist):
        #Definir la funcion como deb ser
        return(x_dist, y_dist)

    def calculate_y_distance(self, x_dist, y_dist):
        #Definir la funcion como deb ser
        return(x_dist, y_dist)
    
    def neight_to_list(self,key):
        return [(item[0].id, item[1]) for item in self.neighbords[key]]

    def to_list(self):
        return [
            self.embledding,
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
        id: {self.id}\n\
        pos: {self.position}\n\
        left: {self.left}\n\
        right: {self.right}\n\
        top: {self.top}\n\
        buttom: {self.buttom}\n\
        '
    
    def print_neighbords(self):
        # print(f'#### {self} ####')
        for key, value in zip(self.neighbords.keys(), self.neighbords.values()):
            if len(self.neighbords[key]) > 0:
                print(f'{key}:')
            for neigh in value:
                print(f'\t{neigh}')
    
    def __str__(self) -> str:
        return f'image {self.id}'
    
    def __repr__(self) -> str:
        return f'image {self.id}'
    
class ImageFeature:
    def __init__(self) -> None:
        self.images:list[ImageEmbedding] = []

    def from_list(self, list_images):
        self.images = []

        for feature in list_images:
            image = ImageEmbedding(None, feature[1])    
            image.set_embedding(feature[0])
            image.set_id(self.len())
            self.images.append(image)
        
        for i, feature in zip(range(self.len()),list_images):
            image = self.images[i]
            for neigh in feature[2][0]: image.neighbords['left'].append(self.convert_to_neighbord(neigh))
            for neigh in feature[2][1]: image.neighbords['right'].append(self.convert_to_neighbord(neigh))
            for neigh in feature[2][2]: image.neighbords['top'].append(self.convert_to_neighbord(neigh))
            for neigh in feature[2][3]: image.neighbords['buttom'].append(self.convert_to_neighbord(neigh))
            for neigh in feature[2][4]: image.neighbords['in'].append(self.convert_to_neighbord(neigh))

    def to_list(self):
        return [image.to_list() for image in self.images]
    
    def add_image(self, image:ImageEmbedding):
        image.set_id(self.len())
        self.images.append(image)

    def get_image_from_id(self, id):
        return self.images[id]
    
    def convert_to_neighbord(self, neigh):
        return (self.get_image_from_id(neigh[0]), neigh[1])
    
    def len(self):
        return len(self.images)
    
    def set_neighbords(self):
        for image in self.images:
            image.set_neighbords(self.images)
            