from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import pandas as pd
import numpy as np
import array
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
from PIL import Image
import os
from pylab import *
import re
import joblib
from PIL import Image, ImageChops, ImageEnhance
from Image_Tampering_Detector.settings import MEDIA_ROOT


# Create your views here.
# model = joblib.load(".\model.sav")

import tensorflow as tf
path = './model.h5'
# model.save(path )
model= tf.keras.models.load_model(path )

def convert_to_ela_image(path, quality):
    filename = path
    resaved_filename = filename.split('.')[0] + '.resaved.jpg'
    ELA_filename = filename.split('.')[0] + '.ela.png'
    
    im = Image.open(filename).convert('RGB')
    im.save(resaved_filename, 'JPEG', quality=quality)
    resaved_im = Image.open(resaved_filename)
    
    ela_im = ImageChops.difference(im, resaved_im)
    
    extrema = ela_im.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    if max_diff == 0:
        max_diff = 1
    scale = 255.0 / max_diff
    
    ela_im = ImageEnhance.Brightness(ela_im).enhance(scale)
    
    return ela_im

def index(request):
    context={'a':1}
    return render(request,'index.html',context)
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import *


def predictImage(request):

    fileObj=request.FILES['filePath']
    fs=FileSystemStorage()
    filePathName1=fs.save(fileObj.name,fileObj)
    filePathName=fs.url(filePathName1)
    # path = askopenfilename()
    path=os.path.join(MEDIA_ROOT,filePathName1)

    print("it is a filepathname---------------------",path)
    print("path------------",path)
    X = []
    X.append(array(convert_to_ela_image(path, 90).resize((128, 128))).flatten() / 255.0)
    X = np.array(X)
    X = X.reshape(-1, 128, 128, 3)
    prediction=np.argmax(model.predict(X))
    labels=['Original','Tampered']
    final_output=labels[prediction]



    context={'filePathName':filePathName,"filePathName1":filePathName1,"final_output":final_output}
    # context={"final_output":final_output}

    if(final_output=='Original'):
        # return render(request,'result_neg.html',context)
        return render(request,'original.html',context)
    elif(final_output=='Tampered'):
        # return render(request,'result_pos.html',context)
        return render(request,'tampered.html',context)


def viewDataBase(request):
    listofimages=os.listdir('./media/')
    listofimagespath=['./media/'+i for i in listofimages]
    context={'listofimagespath':listofimagespath}

    return render(request,'viewDB.html',context)
