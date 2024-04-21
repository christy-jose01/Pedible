"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

from pathlib import Path
import hashlib
import google.generativeai as genai
import json

genai.configure(api_key="AIzaSyD8qggLp527dQm2UCLcA-5nNN12dWgTF6I")

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

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

system_instruction = "You are a pet nutritionist and you specialize heavily in dogs"

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              system_instruction=system_instruction,
                              safety_settings=safety_settings)

uploaded_files = []
def upload_if_needed(pathname: str) -> list[str]:
  path = Path(pathname)
  hash_id = hashlib.sha256(path.read_bytes()).hexdigest()
  try:
    existing_file = genai.get_file(name=hash_id)
    return [existing_file]
  except:
    pass
  uploaded_files.append(genai.upload_file(path=path, display_name=hash_id))
  return [uploaded_files[-1]]

filepath = "Images/IMG_6814.jpg"
uploaded_file = genai.upload_file(path=filepath, display_name="uploaded image")
#upload = upload_if_needed()
#print(upload.name)

prompt_parts = [
  #*upload_if_needed("Images/something.jpg"),
    uploaded_file,
#   """ Check to see if this image even shows food. Output yes or no.
#   For the JSON, the output should be stored in a boolean type variable called isFood. An example would be {"isFood": True}""",
    """Tell me if the image is something that is edible for a dog and store it into isEdible.
    Give me the good or bad reasons (dependent on isEdible) and store it into reason.
    Classify the severity of the food and store it into severity. Should be between Most Severe, Medium Severity, Least Severe.
    Output a JSON file with the format of {'isEdible': boolean, 'reason': string, 'severity': string}
    An example: {'isEdible': False, 'reason': 'Chocolate is bad for dogs.', 'severity': 'Most Severe'}"""
]

#branch1_prompts = 

response = model.generate_content(prompt_parts)
print(response)
bool_response = json.loads(response.text)
print(response.text)
print(bool_response)

if bool_response["isEdible"]:
  print("This is edible")

else:
  print("This is NOT edible") 

# print(response.text)
for uploaded_file in uploaded_files:
  genai.delete_file(name=uploaded_file.name)