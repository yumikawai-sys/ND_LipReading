# Install ffmpeg to your PC and find the path
# C:\Users\Yumi\Documents\ffmpeg-master-latest-win64-gpl-shared\bin

import dlib
import cv2
import os
import numpy as np
from tqdm import tqdm
from align_mouth import landmarks_interpolate, crop_patch, write_video_ffmpeg
# from IPython.display import HTML
from base64 import b64encode

def detect_landmark(image, detector, predictor):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    rects = detector(gray, 1)
    coords = None
    for (_, rect) in enumerate(rects):
        shape = predictor(gray, rect)
        coords = np.zeros((68, 2), dtype=np.int32)
        for i in range(0, 68):
            coords[i] = (shape.part(i).x, shape.part(i).y)
    return coords

def preprocess_video(input_video_path, output_video_path, face_predictor_path, mean_face_path):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(face_predictor_path)
    STD_SIZE = (256, 256)
    mean_face_landmarks = np.load(mean_face_path)
    stablePntsIDs = [33, 36, 39, 42, 45]

    cap = cv2.VideoCapture(input_video_path)
    frames = []
    landmarks = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
        landmark = detect_landmark(frame, detector, predictor)
        landmarks.append(landmark)

    cap.release()

    preprocessed_landmarks = landmarks_interpolate(landmarks)

    # wanted to change width & height (360、288), but didn't work for some reason
    rois = crop_patch(input_video_path, preprocessed_landmarks, mean_face_landmarks, stablePntsIDs, STD_SIZE,
                  window_margin=12, start_idx=48, stop_idx=68, crop_height=96, crop_width=96)
    
    fps = 25
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (96, 96))

    for roi in rois:
        out.write(roi)

    print('out_before', out)
    out.release()

    return

def resize_and_convert(input_video_path, output_video_path, width, height, fps=25):
    cap = cv2.VideoCapture(input_video_path)
    fourcc = cv2.VideoWriter_fourcc(*'MPEG-2')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        resized_frame = cv2.resize(frame, (width, height))  
        out.write(resized_frame)

    cap.release()
    out.release()

mouth_roi_path = './data/roi.mp4'
origin_clip_path = mouth_roi_path

output_mpg_path = "./data/roi_converted.mpg"

if (mouth_roi_path):
    resize_and_convert(origin_clip_path, output_mpg_path, width=360, height=288)
else:
    print('There is no mp4 file before converting')