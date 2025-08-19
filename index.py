from transformers import Blip2Processor, Blip2ForConditionalGeneration
from PIL import Image

processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b")

image = Image.open("example.jpg")
prompt = "create 4 lines of caption for this image"
inputs = processor(images=image, text=prompt, return_tensors="pt")
out = model.generate(**inputs, max_new_tokens=100)
caption = processor.decode(out[0], skip_special_tokens=True)

print("Generated Caption: ", caption)