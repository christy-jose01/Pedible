import urllib
from PIL import Image
from timm.data import resolve_data_config
from timm.data.transforms_factory import create_transform
import requests
from transformers import BeitImageProcessor, BeitForImageClassification
from gemini import gemini


#url, filename = ("https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Milka_Alpine_Milk_Chocolate_bar_100g.jpg/1200px-Milka_Alpine_Milk_Chocolate_bar_100g.jpg", "choco.jpg")
#urllib.request.urlretrieve(url,filename)
#img = Image.open(filename).convert('RGB')

processor = BeitImageProcessor.from_pretrained('microsoft/beit-base-patch16-224-pt22k-ft22k')
model = BeitForImageClassification.from_pretrained('microsoft/beit-base-patch16-224-pt22k-ft22k')

inputs = processor(images=img, return_tensors="pt")
outputs = model(**inputs)
logits = outputs.logits
# model predicts one of the 21,841 ImageNet-22k classes
predicted_class_idx = logits.argmax(-1).item()
model_prediction = model.config.id2label[predicted_class_idx]
response = gemini(model_prediction,img)
