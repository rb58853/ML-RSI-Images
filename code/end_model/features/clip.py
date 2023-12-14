from imodel import IModel

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