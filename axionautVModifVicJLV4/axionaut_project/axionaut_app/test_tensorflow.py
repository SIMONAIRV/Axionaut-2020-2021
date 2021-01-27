import tensorflow
from keras.models import load_model
try:
    model = load_model("../models/model_test3.h5")
    print(model.summary())
except:
    print("Error!")