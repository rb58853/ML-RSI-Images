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