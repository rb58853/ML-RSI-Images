from imodel import IModel
from sam import SAM

class BLIP(IModel):
    '''
    ## BLIP()
    ### Funciones:
    - `import_model`: 
        importa el modelo de BLIP, asignando valores a `MODEL` y `PROCESSOR`.
    - `caption`: 
        recibe una imagen y devuelve una descipcion en lenguaje natural, en formato de texto. 
    - `all_captions`: 
        recibe una imagen y un tipo de segmentacion, devuelve una lista de descripciones de cada una de las segmentaciones dadas por SAM.  
    -  `all_captions_from_list_images`:
        recibe una imagen (la principal sin segmentar) y una lista de imagenes previamente segmentadas en SAM, devuele una lista de descripciones de estas imagenes.
    '''
    PROCESSOR = None
    MODEL = None

    def import_model(local = False):
        '''
            Carga el modelo desde la biblioteca transformers en caso de `local = False` 
        '''
        if not local:
            from transformers import BlipProcessor, BlipForConditionalGeneration
            BLIP.PROCESSOR = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
            BLIP.MODEL = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to("cuda")
        else:
            pass #TODO importar el modelo desde drive

    #Se cambio blip por caption
    def caption (image):
        inputs = BLIP.PROCESSOR(image, return_tensors="pt").to("cuda")
        out = BLIP.MODEL.generate(**inputs)
        result = BLIP.PROCESSOR.decode(out[0], skip_special_tokens=True)
    
        if result[:9] == "there is ":
            result = result[9:]
        return result
    
    def all_captions(image, raw_image, segmentation = 'box', min_area = 0, min_box_area = 0):
        '''
            ### INPUTS:\n
            - `image`: imagen cargada con cv2 \n
            - `raw_image`: imagen cargada con PIL.Image\n
            - `segmentation`: tipo de segmentacion que se va a utilizar para seleccionar imagenes (`'box'` o `'mask'`)\n
            - `min_area`: area minima en pixeles de tamaño que puede puede tener las imagenes segmentadas \n
            - `min_box_area`: area minima en pixeles de tamaño que puede puede tener un cuadro que contiene una imagen segmentada \n

            ### OUTPUTS: \n
            - `list` = `[`lista con cada una de las descripciones de las imagenes segmentadas agregada al a descripcion principal`]`
        '''

        origin = str(BLIP.caption(raw_image))
        captions = [origin]
    
        areas = SAM.all_areas_from_image(image, raw_image, min_area,min_box_area)[segmentation]
        for im in areas:
            captions.append(origin +" "+ str(BLIP.caption(im)))
        return captions
    
    def all_captions_from_list_images(raw_image, segmented_images):
        '''

        '''
        origin = str(BLIP.caption(raw_image))
        captions = [origin]
        for image in segmented_images:
            caption = str(BLIP.caption(image))
            captions.append(origin +" "+ caption)
        return captions    

