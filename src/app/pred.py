# (pls. use the specified version)
# pip install the following 
# pip install numpy==1.24.1
# pip install opencv-python==4.6.0.66
# pip install tensorflow==2.10.1
# pip install scikit-image

import os 
import cv2
import tensorflow as tf
import numpy as np
from typing import List
from app.utils import load_data, num_to_char
from app.modelutil import load_model

# Set the video file path
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'data', 's1', 'bbaf2n.mpg')
# file_path = './data/s1/bbaf2n.mpg'
# file_path = './data/s1/yumivideo.mpg'
video = load_data(tf.convert_to_tensor(file_path))
print('file_path', file_path)
print('video', video)

vocab = [x for x in "abcdefghijklmnopqrstuvwxyz'?!123456789 "]
char_to_num = tf.keras.layers.StringLookup(vocabulary=vocab, oov_token="")
num_to_char = tf.keras.layers.StringLookup(
    vocabulary=char_to_num.get_vocabulary(), oov_token="", invert=True
)

print(
    f"The vocabulary is: {char_to_num.get_vocabulary()} "
    f"(size ={char_to_num.vocabulary_size()})"
)
char_to_num.get_vocabulary()

# load model & predict
def sample_prediction():
    model = load_model()
    yhat = model.predict(tf.expand_dims(video, axis=0))
    decoder = tf.keras.backend.ctc_decode(yhat, [75], greedy=True)[0][0].numpy()

    converted_prediction = tf.strings.reduce_join(num_to_char(decoder)).numpy().decode('utf-8')
    print('prediction', converted_prediction)

    return converted_prediction

