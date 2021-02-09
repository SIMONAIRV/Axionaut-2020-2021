from numpy import asarray
from PIL import Image
from os import listdir
from os.path import isfile, join

def normalisation(img):

    return img/255

def horizontal_flip(img):

    return np.fliplr(img)

def get_opposite(folder):

    if folder == "Right":
        return "Left"
    elif folder == "Left":
        return "Right"
    elif folder == "Hard Right":
        return "Hard Left
    elif folder == "Hard Left":
        return "Hard Right"
    else:
        return "Straight"

folder_names = [name for name in os.listdir(".")] # replace . by the path of the folder.

for folder in folder_names:
    imgs = [f for f in listdir("Path/"+ folder), if isfile(join("Path/"+folder, f))]
    for img in imgs:
        print(img) # Get the name of the image name = 
        img = Image.open(img)
        img = asarray(img)
        img = normalisation(img)
        img = horizontal_flip(img)
        img = Image.fromarray(img)
        img.save("Path" + str(get_opposite(folder)+"name of the image" + "_inversed.jpg")) #jpg or png.

