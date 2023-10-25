from PIL import Image

def mask_image(mask, raw_image):
    weigth, heigth = raw_image.size
    new_image = Image.new('RGB', (weigth, heigth))
    for i in range (len(raw_image)):
        for j in range (len(raw_image[i])):
            if mask[i][j]:
                new_image[i][j] = raw_image[i][j]
            else:
                new_image[i][j] = 0
    return new_image