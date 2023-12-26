from caption_models.imodel import IModel
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

    def import_model(own = False, dir = '/content/gdrive/My Drive/Images-RI-ML/image_caption_models/BLIP/'):
        '''
            Carga el modelo desde la biblioteca transformers en caso de `own = False` 
        '''
        if not own:
            from transformers import BlipProcessor, BlipForConditionalGeneration
            BLIP.PROCESSOR = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
            BLIP.MODEL = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to("cuda")
        else:
            from transformers import BlipProcessor, BlipForConditionalGeneration
            BLIP.PROCESSOR = BlipProcessor.from_pretrained(dir + 'processor')
            BLIP.MODEL = BlipForConditionalGeneration.from_pretrained(dir + 'model').to("cuda")
    
    def save(dir = '/content/gdrive/My Drive/Images-RI-ML/image_caption_models/BLIP/'):
        BLIP.MODEL.save_pretrained(dir + "model")
        BLIP.PROCESSOR.save_pretrained(dir + "processor")
    
    def caption (image, max_tokens = 50, prompt = ""):
        inputs = BLIP.PROCESSOR(image, return_tensors="pt").to("cuda")
        out = BLIP.MODEL.generate(**inputs)
        result = BLIP.PROCESSOR.decode(out[0], skip_special_tokens=True)
    
        if result[:9] == "there is ":
            result = result[9:]
        return result
