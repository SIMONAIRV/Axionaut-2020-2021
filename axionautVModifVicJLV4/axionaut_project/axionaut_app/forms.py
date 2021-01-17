from django import forms
import json
import os

CONFIG = './config.json'
with open(CONFIG) as json_file:
    config = json.load(json_file)
    MODELS_PATH = config['models_path']

models = []
print(os.path.isdir(MODELS_PATH))
if os.path.isdir(MODELS_PATH):
    #models = [os.path.join(MODELS_PATH, f) for f in os.listdir(MODELS_PATH) if f.endswith('.hdf5')]
    models = [f for f in os.listdir(MODELS_PATH)]


list_tuples = []
for i in range(0, len(models)):
    list_tuples.append((i, models[i]))
model_choices = tuple(list_tuples)


class ModelsForm(forms.Form):
    Models = forms.ChoiceField(choices=model_choices)
