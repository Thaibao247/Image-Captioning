from flask import Flask, Response, render_template, flash, request, redirect, url_for
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.models import Model
from keras.applications.inception_v3 import preprocess_input
from pickle import dump, load
from tensorflow.keras.models import load_model
import re
import os
import uuid
import requests
#from WhiteNoise import WhiteNoise
import cv2
import numpy as np
import argparse
from werkzeug.utils import secure_filename
from flask import (Flask, flash, redirect, render_template, request,
                   send_from_directory, url_for)
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from time import time
from numpy import array
from tensorflow.keras.utils import to_categorical


from flask import Flask, render_template, request
import cv2
from keras.models import load_model
import numpy as np
from keras.applications import ResNet50
from keras.optimizers import Adam
from keras.layers import Dense, Flatten, Input, Convolution2D, Dropout, LSTM, TimeDistributed, Embedding, Bidirectional, Activation, RepeatVector, Concatenate
from keras.models import Sequential, Model
from tensorflow.keras import utils as np_utils
from keras.preprocessing import image, sequence
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tqdm import tqdm


vocab = np.load(
    'D:\\University\\ImageCaptioning\\caption-it\\vocab.npy', allow_pickle=True)
vocab = vocab.item()
inv_vocab = {v: k for k, v in vocab.items()}


print("vocabulary loaded")


embedding_size = 128
vocab_size = len(vocab)
max_len = 36


image_model = Sequential()
image_model.add(Dense(embedding_size, input_shape=(2048,), activation='relu'))
image_model.add(RepeatVector(max_len))


language_model = Sequential()
language_model.add(Embedding(input_dim=vocab_size,
                   output_dim=embedding_size, input_length=max_len))
language_model.add(LSTM(256, return_sequences=True))
language_model.add(TimeDistributed(Dense(embedding_size)))


conca = Concatenate()([image_model.output, language_model.output])
x = LSTM(128, return_sequences=True)(conca)
x = LSTM(512, return_sequences=False)(x)
x = Dense(vocab_size)(x)
out = Activation('softmax')(x)
model = Model(inputs=[image_model.input, language_model.input], outputs=out)
model.compile(loss='categorical_crossentropy',
              optimizer='RMSprop', metrics=['accuracy'])
model.load_weights(
    'D:\\University\\ImageCaptioning\\caption-it\\model_weights.h5')

print("MODEL LOADED")

resnet = ResNet50(include_top=False, weights='imagenet',
                  input_shape=(224, 224, 3), pooling='avg')


print("RESNET MODEL LOADED")


app = Flask(__name__)

UPLOAD_FOLDER = 'static/images/'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        image = cv2.imread('static/images/'+filename)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (224, 224))
        image = np.reshape(image, (1, 224, 224, 3))
        incept = resnet.predict(image).reshape(1, 2048)
        print("Predict Features")
        text_in = ['startofseq']
        final = ''
        print("GETING Captions")
        count = 0
        while tqdm(count < 20):
            count += 1
            encoded = []
            for i in text_in:
                encoded.append(vocab[i])

            padded = pad_sequences(
                [encoded], maxlen=max_len, padding='post', truncating='post').reshape(1, max_len)

            sampled_index = np.argmax(model.predict([incept, padded]))

            sampled_word = inv_vocab[sampled_index]

            if sampled_word != 'endofseq':
                final = final + ' ' + sampled_word

            text_in.append(sampled_word)
        params = {
            'content': "static/images/" + filename,
            'caption': final.strip().capitalize(),
        }
        return render_template('image.html', **params)
       # return render_template('image.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/<filename>')
def display_image(filename):
    # cap = cv2.VideoCapture(filename)
    params = {
        'content': "static/images/" + filename,
        'caption': "Hello",
        'tr_caption': "Hello",
    }
    return render_template('success.html', **params)


@app.route('/image-Detect')
def imageDetect():
    return render_template('image.html')


if __name__ == '__main__':
    app.run(debug=True)
