from transformers import AutoProcessor, Blip2ForConditionalGeneration
import torch
import requests
from PIL import Image

blip2_processor = AutoProcessor.from_pretrained("Salesforce/blip2-opt-2.7b")
blip2_model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b", torch_dtype=torch.float16) 
device = "cuda" if torch.cuda.is_available() else "cpu"
blip2_model.to(device)

img_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/demo.jpg' 
raw_image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')

def blip2 (image):
    inputs = blip2_processor(image, return_tensors="pt").to(device, torch.float16)
    generated_ids = blip2_model.generate(**inputs, max_new_tokens=20)
    generated_text = blip2_processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
    return generated_text