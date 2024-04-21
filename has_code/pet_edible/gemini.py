import pathlib
import textwrap
from PIL import Image
import urllib
import google.generativeai as genai
import json

from IPython.display import display
from IPython.display import Markdown

def gemini(model_prediction, ImageToParse):
    def to_markdown(text):
        text = text.replace('•', '  *')
        return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


    GOOGLE_API_KEY='AIzaSyB6-q8MbRpsb66XPZtaZlNgCYIlStm929Q'

    genai.configure(api_key=GOOGLE_API_KEY)

    safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE"
  },
]

    model = genai.GenerativeModel('gemini-1.5-pro-latest',generation_config={"response_mime_type" : "application/json"},safety_settings=safety_settings)

    img = ImageToParse

    prompt = f"""Tell me if the image is {model_prediction} and it is something edible for a dog and store it into isEdible. Do NOT store as a string or any other data type, only as a boolean.
    Give me the good or bad reasons (dependent on isEdible) and store it into reason. If it is a popular brand, say what the food item is. For example, if it's an Oreo, say that it is.
    Classify the severity of the food and store it into severity. Should be between Most Severe, Medium Severity, Moderate, Healthy.
    Output a JSON file with the format of {{'isEdible': boolean, 'reason': string, 'severity': string}}
    An example: {{'isEdible': False, 'reason': 'Chocolate is bad for dogs.', 'severity': 'Most Severe'}}"""

    response = model.generate_content([prompt, img], stream=True)
    response.resolve()
    # print(response)
    print(response.text)
    return json.loads(response.text)