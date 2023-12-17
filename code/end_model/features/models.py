from PIL import Image
import torch
import numpy as np
import matplotlib.pyplot as plt
import cv2

class IModel:
    def import_model():
        pass
    def save(dir):
        pass

class SAM(IModel):
    '''
    ## SAM
    ### Funciones
    - `import_model`: importa el modelo SAM, asigna un valor a `MASK_GENERATOR`
    '''
    MASK_GENERATOR = None
    
    def import_model():
        import torchvision
        print("PyTorch version:", torch.__version__)
        print("Torchvision version:", torchvision.__version__)
        print("CUDA is available:", torch.cuda.is_available())
        import sys
        
        import sys
        sys.path.append("..")
        from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor
        
        sam_checkpoint = "sam_vit_h_4b8939.pth"
        model_type = "vit_h"
        
        device = "cuda"
        
        sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
        sam.to(device=device)
        
        SAM.MASK_GENERATOR = SamAutomaticMaskGenerator(
            model=sam,
            points_per_side=32,
            pred_iou_thresh=0.86,
            stability_score_thresh=0.92,
            crop_n_layers=1,
            crop_n_points_downscale_factor=2,
            min_mask_region_area=100,  # Requires open-cv to run post-processing
        )

    def mask_image(mask, raw_image, bbox):
        weigth, heigth = raw_image.size
        new_image = Image.new('RGBA', (weigth, heigth), (0, 0, 0, 0))

        original_pixles = raw_image.load()
        pixels = new_image.load()

        for i in range (heigth):
            for j in range (weigth):
                if mask[i,j]:
                    pixels[j, i] = original_pixles[j,i]
                else:
                    pass

        x,y,w,h =  bbox[0],bbox[1],bbox[2],bbox[3]
        return new_image.crop((x,y,x+w,y+h))

    def bbox_image(bbox, image):
        x,y,w,h =  bbox[0],bbox[1],bbox[2],bbox[3]
        return image[y:y+h, x:x+w]
    
    # def mask_caption(mask, raw_image,bbox):
    #     return BLIP.caption(SAM.mask_image(mask, raw_image,bbox))

    # def bbox_caption(bbox, image):
    #     return BLIP.caption(SAM.bbox_image(bbox, image))

    def all_areas_from_image(image, raw_image, min_area = 0, min_box_area = 0):
        """
        ### INPUTS:\n
        `image`: imagen cargada con cv2 \n
        `raw_image`: imagen cargada con PIL.Image \n
        `min_area`: area minima en pixeles de tamaño que puede puede tener las imagenes segmentadas \n
        `min_box_area`: area minima en pixeles de tamaño que puede puede tener un cuadro que contiene una imagen segmentada \n

        ### OUTPUTS: \n
        `dict` = \n
        `{` \n
          `'box'`: imagenes(cuadro comprendido en segmentacion), \n
          `'mask'`: imagenes(solo segmentacion fondo transparente) \n
        `}` \n
        """
        masks = SAM.MASK_GENERATOR.generate(image)
        images_box= []
        images_mask= []
        for mask in masks:
            box_im = SAM.bbox_image(mask['bbox'],image)
            h, w, c = box_im.shape
            box_area = h * w
            if box_area >= min_box_area:
                images_box.append(box_im)
            if mask['area'] >= min_area:
                images_mask.append(SAM.mask_image(mask['segmentation'], raw_image, mask['bbox']))
        return {'box':images_box, 'mask':images_mask}

    def all_masks_from_sam(image, min_area = 0, min_box_area = 0):
        masks = SAM.MASK_GENERATOR.generate(image)
        _masks = [mask for mask in masks]
        index = 0
        for mask in masks:
            bbox = mask['bbox']
            x,y,w,h =  bbox[0],bbox[1],bbox[2],bbox[3]
            box_area = h * w
            if box_area < min_box_area or mask['area'] < min_area:
               _masks.remove(mask)
               index -=1
            index+=1
        return _masks    

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

    def import_model(local = False, dir = '/content/gdrive/My Drive/image_caption_models/BLIP/'):
        '''
            Carga el modelo desde la biblioteca transformers en caso de `local = False` 
        '''
        if not local:
            from transformers import BlipProcessor, BlipForConditionalGeneration
            BLIP.PROCESSOR = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
            BLIP.MODEL = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to("cuda")
        else:
            from transformers import BlipProcessor, BlipForConditionalGeneration
            BLIP.PROCESSOR = BlipProcessor.from_pretrained(dir + 'processor')
            BLIP.MODEL = BlipForConditionalGeneration.from_pretrained(dir + 'model').to("cuda")
    
    def save(dir = '/content/gdrive/My Drive/image_caption_models/BLIP/'):
        BLIP.MODEL.save_pretrained(dir + "model")
        BLIP.PROCESSOR.save_pretrained(dir + "processor")
    
    def caption (image):
        inputs = BLIP.PROCESSOR(image, return_tensors="pt").to("cuda")
        out = BLIP.MODEL.generate(**inputs)
        result = BLIP.PROCESSOR.decode(out[0], skip_special_tokens=True)
    
        if result[:9] == "there is ":
            result = result[9:]
        return result
    
    def all_captions(image, raw_image, segmentation = 'box', min_area = 0, min_box_area = 0):
        '''
            #### INPUTS:\n
            - `image`: imagen cargada con cv2 \n
            - `raw_image`: imagen cargada con PIL.Image\n
            - `segmentation`: tipo de segmentacion que se va a utilizar para seleccionar imagenes (`'box'` o `'mask'`)\n
            - `min_area`: area minima en pixeles de tamaño que puede puede tener las imagenes segmentadas \n
            - `min_box_area`: area minima en pixeles de tamaño que puede puede tener un cuadro que contiene una imagen segmentada \n

            #### OUTPUTS: \n
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

class BLIP2(IModel):
    '''
    ## BLIP-2
    
    ### Funciones:
    - `import_model`: 
        importa el modelo de BLIP2, asignando valores a `MODEL`, `PROCESSOR` y `DEVICE`.
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

    def import_model(local = False, dir = "/content/gdrive/My Drive/image_caption_models/BLIP2/"):
        '''
            Carga el modelo desde la biblioteca transformers en caso de `local = False` 
        '''
        if not local:
            from transformers import AutoProcessor, Blip2ForConditionalGeneration
            BLIP2.PROCESSOR = AutoProcessor.from_pretrained("Salesforce/blip2-opt-2.7b")
            BLIP2.MODEL = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b", torch_dtype=torch.float16)
            BLIP2.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
            BLIP2.MODEL.to(BLIP2.DEVICE)
        else:
            from transformers import AutoProcessor, Blip2ForConditionalGeneration
            BLIP2.PROCESSOR = AutoProcessor.from_pretrained(dir+'processor')
            BLIP2.MODEL = Blip2ForConditionalGeneration.from_pretrained(dir + 'model', torch_dtype=torch.float16)
            BLIP2.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
            BLIP2.MODEL.to(BLIP2.DEVICE)
    
    def save(dir = '/content/gdrive/My Drive/image_caption_models/BLIP2/'):
        BLIP2.MODEL.save_pretrained(dir + "model")
        BLIP2.PROCESSOR.save_pretrained(dir + "processor")

    def caption (image, prompt = "Describe the image in detail"):
        # inputs = BLIP2.PROCESSOR(image, text=prompt, return_tensors="pt").to(BLIP2.DEVICE, torch.float16)
        # generated_ids = BLIP2.MODEL.generate(**inputs)
        inputs = BLIP2.PROCESSOR(image, return_tensors="pt").to(BLIP2.DEVICE, torch.float16)
        generated_ids = BLIP2.MODEL.generate(**inputs, max_new_tokens=20)
        generated_text = BLIP2.PROCESSOR.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
        return generated_text
    
    def all_captions(image, raw_image, segmentation = 'box', min_area = 0, min_box_area = 0):
        '''
            #### INPUTS:\n
            - `image`: imagen cargada con cv2 \n
            - `raw_image`: imagen cargada con PIL.Image\n
            - `segmentation`: tipo de segmentacion que se va a utilizar para seleccionar imagenes (`'box'` o `'mask'`)\n
            - `min_area`: area minima en pixeles de tamaño que puede puede tener las imagenes segmentadas \n
            - `min_box_area`: area minima en pixeles de tamaño que puede puede tener un cuadro que contiene una imagen segmentada \n

            #### OUTPUTS: \n
            - `list` = `[`lista con cada una de las descripciones de las imagenes segmentadas agregadas a la descripcion principal`]`
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

class CLIP(IModel):
    '''
    ## CLIP

    '''    
    PROCESSOR = None
    MODEL = None
    DEVICE = None

    def import_model():
        from transformers import CLIPProcessor, CLIPModel
        CLIP.MODEL = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        CLIP.PROCESSOR = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

        CLIP.DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        CLIP.MODEL = CLIP.MODEL.to(CLIP.DEVICE)

    def select_caption(captions, image):
        """
        Usando el modelo CLIP selecciona la mejor descripcion de la lista de descripciones

        INPUTS:\n
        `captions`: lista de descripciones(texto) \n
        `image`: imagen a la cual hallar similitud con los textos\n

        OUTPUTS:\n
        `dict`:\n
        `{`\n
        'caption': texto con mayor similitud con la imagen (`str`)\n
        'probs': la lista de probabilidades que devuelve CLIP para esa imagen y textos(`list`) \n
        `}`
        """
        inputs = CLIP.PROCESSOR(text=captions, images=image, return_tensors="pt", padding=True)
        inputs = {name: tensor.to(CLIP.DEVICE) for name, tensor in inputs.items()}
        outputs = CLIP.MODEL(**inputs)

        logits_per_image = outputs.logits_per_image  # this is the image-text similarity score
        probs = logits_per_image.softmax(dim=1)
        return {'caption':CLIP.select_from_probs(probs, captions), 'probs': probs[0]}

    def select_from_probs(probs, captions):
        max_prob = 0
        index = 0
        for i,prob in zip(range(len(probs[0])),probs[0]):
            if prob > max_prob:
                max_prob = prob
                index = i
        return captions[index]

    def reduce_caption(caption, image):
        """
        Dada una descripcion se procesa la misma eliminando palabras innecesarias, se decide si la palabra es necesaria o no hallando similitud con CLIP\n

        INPUTS:\n
        `caption`: texto que se desea procesar\n
        `image`: imagen con la cual se desea hallar la similitud\n

        OUTPUTS:\n
        `str`: Nueva descripcion con palabras eliminadas
        """
        split = caption.split(' ')
        for word in split:
            temp = caption.split(' ')
            temp.remove(word)
            temp = ' '.join(temp)

            inputs = CLIP.PROCESSOR(text=[temp, caption], images=image, return_tensors="pt", padding=True)
            inputs = {name: tensor.to(CLIP.DEVICE) for name, tensor in inputs.items()}
            outputs = CLIP.MODEL(**inputs)
            logits_per_image = outputs.logits_per_image
            probs = logits_per_image.softmax(dim=1)

            if probs[0][0]> probs[0][1]:
                caption = temp
        return caption    
    
    def short_captions(probs,captions):
        '''
        Ordena las descripciones usando como criterio de comparacion cual tiene mayor similitud con la imagen. Develve la lista de estos comop un diccionario `prob: caption` en orden de mejor similitud a peor similitud \n
        INPUTS:\n
        `probs`: lista de probabilidades en orden original \n
        `captions`: lista de descripciones en orden original\n
        OUTPUTS:\n
        `dict`= `{` porb(`float`): descripcion(`str`)`}`
        '''
        _probs = [prob.item() for prob in probs]
        for i in range(len(captions)):
            for j in range(i+1, len(captions)):
                if _probs[j]>_probs[i]:
                    temp_p= _probs[i]
                    temp_c = captions[i]
                    _probs[i] = _probs[j]
                    captions[i] = captions[j]
                    _probs[j] = temp_p
                    captions[j] = temp_c
        return {prob: caption for prob,caption in zip(_probs,captions) }