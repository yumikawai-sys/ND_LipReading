import cv2
import subprocess

def convert_to_mpg(input_video_path, output_video_path):
    
    cap = cv2.VideoCapture(input_video_path)

    # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = 360
    height = 288
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    fourcc = cv2.VideoWriter_fourcc(*'MPG1')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()

    subprocess.run(['ffmpeg', '-i', output_video_path, output_video_path.replace('.mpg', '.mp4')])

input_video_path = 'yumivideo.mp4'
output_video_path = 'roi.mpg'

convert_to_mpg(input_video_path, output_video_path)
