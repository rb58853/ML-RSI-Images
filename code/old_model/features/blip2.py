from imodel import IModel
from sam import SAM

class BLIP2(IModel):
    '''
    ## BLIP-2
    
    ### Funciones:
    - `import_model`: 
        importa el modelo de BLIP, asignando valores a `MODEL`, `PROCESSOR` y `DEVICE`.
    - `caption`: 
        recibe una imagen y devuelve una descipcion en lenguaje natural, en formato de texto. 
    - `all_captions`: 
        recibe una imagen y un tipo de segmentacion, devuelve una lista de descripciones de cada una de las segmentaciones dadas por SAM.  
    -  `all_captions_from_list_images`:
        recibe una imagen (la principal sin segmentar) y una lista de imagenes previamente segmentadas en SAM, devuele una lista de descripciones de estas imagenes.
    '''
    PROCESSOR = None
    MODEL = None
    DEVICE = None

    def import_model(local = False):
        '''
            Carga el modelo desde la biblioteca transformers en caso de `local = False` 
        '''
        if not local:
            from transformers import AutoProcessor, Blip2ForConditionalGeneration
            import torch
            BLIP2.PROCESSOR = AutoProcessor.from_pretrained("Salesforce/blip2-opt-2.7b")
            BLIP2.MODEL = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b", torch_dtype=torch.float16)
            BLIP2.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
            BLIP2.MODEL.to(BLIP2.DEVICE)
        else:
            pass #TODO importar el modelo desde drive

    #Se cambio blip por caption
    def caption (image):
        inputs = BLIP2.PROCESSOR(image, return_tensors="pt").to(BLIP2.DEVICE, torch.float16)
        generated_ids = BLIP2.MODEL.generate(**inputs, max_new_tokens=20)
        generated_text = BLIP2.PROCESSOR.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
        return generated_text

    
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

        origin = str(BLIP2.caption(raw_image))
        captions = [origin]
    
        areas = SAM.all_areas_from_image(image, raw_image, min_area,min_box_area)[segmentation]
        for im in areas:
            captions.append(origin +" "+ str(BLIP2.caption(im)))
        return captions
    
    def all_captions_from_list_images(raw_image, segmented_images):
        '''

        '''
        origin = str(BLIP2.caption(raw_image))
        captions = [origin]
        for image in segmented_images:
            caption = str(BLIP2.caption(image))
            captions.append(origin +" "+ caption)
        return captions    
