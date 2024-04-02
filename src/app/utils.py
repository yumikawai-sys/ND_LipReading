import tensorflow as tf
from typing import List
import cv2
import os 

vocab = [x for x in "abcdefghijklmnopqrstuvwxyz'?!123456789 "]
char_to_num = tf.keras.layers.StringLookup(vocabulary=vocab, oov_token="")
# Mapping integers back to original characters
num_to_char = tf.keras.layers.StringLookup(
    vocabulary=char_to_num.get_vocabulary(), oov_token="", invert=True
)

#### original function from github
def load_video(path:str) -> List[float]: 
    #print(path)
    cap = cv2.VideoCapture(path)
    frames = []
    for _ in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))): 
        ret, frame = cap.read()
        frame = tf.image.rgb_to_grayscale(frame)
        frames.append(frame[190:236,80:220,:])
    cap.release()
    
    mean = tf.math.reduce_mean(frames)
    std = tf.math.reduce_std(tf.cast(frames, tf.float32))
    return tf.cast((frames - mean), tf.float32) / std

# def load_video(path: str) -> tf.Tensor:
#     cap = cv2.VideoCapture(path)
#     frames = []
#     while len(frames) < 75:  # Ensure there are exactly 75 frames
#         ret, frame = cap.read()
#         if not ret:  # If no frame is returned, break the loop
#             break
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
#         frame = frame[190:236, 80:220]  # Crop the frame to focus on the mouth region
#         frame = tf.image.rgb_to_grayscale(frame)  # Convert to grayscale
#         frames.append(frame)
#     cap.release()

#     # Pad or truncate frames to ensure exactly 75 frames
#     if len(frames) < 75:
#         frames += [frames[-1]] * (75 - len(frames))
#     else:
#         frames = frames[:75]

#     # Compute mean and standard deviation
#     frames = tf.stack(frames)
#     mean = tf.math.reduce_mean(frames)
#     std = tf.math.reduce_std(tf.cast(frames, tf.float32))

#     # Normalize frames
#     frames = tf.cast((frames - mean), tf.float32) / std

#     return frames

# def load_video(path: str, target_size: tuple = (288, 360)) -> tf.Tensor:
#     cap = cv2.VideoCapture(path)
#     frames = []
#     while len(frames) < 75:  # Ensure there are exactly 75 frames
#         ret, frame = cap.read()
#         if not ret:  # If no frame is returned, break the loop
#             break
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
#         frame = cv2.resize(frame, target_size)  # Resize the frame
#         frame = frame[170:220, 100:240]  # Adjust cropping to focus on the mouth region
#         frame = tf.image.rgb_to_grayscale(frame)  # Convert to grayscale
#         frames.append(frame)
#     cap.release()

#     # Pad or truncate frames to ensure exactly 75 frames
#     if len(frames) < 75:
#         frames += [frames[-1]] * (75 - len(frames))
#     else:
#         frames = frames[:75]

#     # Compute mean and standard deviation
#     frames = tf.stack(frames)
#     mean = tf.math.reduce_mean(frames)
#     std = tf.math.reduce_std(tf.cast(frames, tf.float32))

#     # Normalize frames
#     frames = tf.cast((frames - mean), tf.float32) / std
#     print(type(frames))
#     return frames

    
def load_alignments(path:str) -> List[str]: 
    print(path)
    with open(path, 'r') as f: 
        lines = f.readlines() 
    tokens = []
    for line in lines:
        line = line.split()
        if line[2] != 'sil': 
            tokens = [*tokens,' ',line[2]]
    return char_to_num(tf.reshape(tf.strings.unicode_split(tokens, input_encoding='UTF-8'), (-1)))[1:]

def load_data(path: str): 
    path = bytes.decode(path.numpy())
    file_name = path.split('/')[-1].split('.')[0]
    video_path = os.path.join('.','data','s1',f'{file_name}.mpg')
    alignment_path = os.path.join('.','data','alignments','s1',f'{file_name}.align')
    frames = load_video(video_path) 
    
    return frames