from PIL import Image
import torch

class SAM:
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
            min_mask_region_area= 20*20,  # Requires open-cv to run post-processing
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
    
    def all_areas_from_image(image, raw_image = None, min_area = 0, min_box_area = 0, use_mask_as_return = False):
        """
        ### INPUTS:\n
        `image`: imagen cargada con cv2 \n
        `raw_image`: imagen cargada con PIL.Image \n
        `min_area`: area minima en pixeles de tamaño que puede puede tener las imagenes segmentadas \n
        `min_box_area`: area minima en pixeles de tamaño que puede puede tener un cuadro que contiene una imagen segmentada \n
        `use_mask_as_return`: usa las mascaras con fondo transparente como parte del resultado de la funcion

        ### OUTPUTS: \n
        `dict` = \n
        `{` \n
          `'box'`: imagenes(cuadro comprendido en segmentacion), \n
          `'mask'`: imagenes(solo segmentacion fondo transparente) Lista vacia si no se usa \n
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
            
            if use_mask_as_return:
                if mask['area'] >= min_area:
                    images_mask.append(SAM.mask_image(mask['segmentation'], raw_image, mask['bbox']))
        
        return {'box':images_box, 'mask':images_mask}

    # [obsolete]
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