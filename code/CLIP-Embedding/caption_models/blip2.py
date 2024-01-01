from caption_models.imodel import IModel
import torch

class BLIP2(IModel):
    '''
    ## BLIP-2
    
    ### Funciones:
    - `import_model`: 
        importa el modelo de BLIP2, asignando valores a `MODEL`, `PROCESSOR` y `DEVICE`.
    - `caption`: 
        recibe una imagen y devuelve una descipcion en lenguaje natural, en formato de texto. 
    '''
    PROCESSOR = None
    MODEL = None
    DEVICE = None

    def import_model(own = False, dir = "/content/gdrive/My Drive/Images-RI-ML/image_caption_models/BLIP2/"):
        '''
            Carga el modelo desde la biblioteca transformers en caso de `own = False` 
        '''
        if not own:
            from transformers import AutoProcessor, Blip2ForConditionalGeneration
            BLIP2.PROCESSOR = AutoProcessor.from_pretrained("Salesforce/blip2-opt-2.7b")
            BLIP2.MODEL = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b", torch_dtype=torch.float16)
            BLIP2.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
            BLIP2.MODEL.to(BLIP2.DEVICE)
        else:
            from transformers import AutoProcessor, Blip2ForConditionalGeneration
            # BLIP2.PROCESSOR = AutoProcessor.from_pretrained(dir+'processor')
            BLIP2.PROCESSOR = AutoProcessor.from_pretrained("Salesforce/blip2-opt-2.7b")
            BLIP2.MODEL = Blip2ForConditionalGeneration.from_pretrained("rb58853/blip2-clip-sam", torch_dtype=torch.float16)
            BLIP2.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
            BLIP2.MODEL.to(BLIP2.DEVICE)
    
    def save(dir = '/content/gdrive/My Drive/Images-RI-ML/image_caption_models/BLIP2/'):
        BLIP2.MODEL.save_pretrained(dir + "model")
        BLIP2.PROCESSOR.save_pretrained(dir + "processor")

    def caption (image, max_tokens = 20 , prompt = "Describe the image in detail"):
        # inputs = BLIP2.PROCESSOR(image, text=prompt, return_tensors="pt").to(BLIP2.DEVICE, torch.float16)
        # generated_ids = BLIP2.MODEL.generate(**inputs)
        inputs = BLIP2.PROCESSOR(image, return_tensors="pt").to(BLIP2.DEVICE, torch.float16)
        generated_ids = BLIP2.MODEL.generate(**inputs, max_new_tokens=max_tokens )
        generated_text = BLIP2.PROCESSOR.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
        return generated_text
    
