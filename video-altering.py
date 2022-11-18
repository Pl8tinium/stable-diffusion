import cv2
from pathlib import Path
import math
import os

def split_video(video_input_path, frames_output_path, desired_framerate, framerate_up_rounding=True):
    video = cv2.VideoCapture(video_input_path)
    current_framerate = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    total_len_in_sec = (total_frames / current_framerate) % 60
    rounding_method = math.ceil if framerate_up_rounding else math.floor
    frame_skip = rounding_method(current_framerate / desired_framerate)
    real_target_framerate = rounding_method(current_framerate / frame_skip)
    print(f'current framerate{current_framerate} | desired framerate {desired_framerate} | actual framerate {real_target_framerate}')
    delay_time=int(1000 / real_target_framerate)
    secondsCounter = 0
    current_frame_nr = 0
    real_frame_nr = 0
    Path(frames_output_path.joinpath(f'/sec{secondsCounter}')).mkdir(parents=True, exist_ok=True)

    while (True):
        success, frame = video.read()
        if not success:
            print("finished! (or error)")
            break
        if (current_frame_nr % frame_skip) == 0:
            real_frame_nr += 1
            cv2.imwrite(frames_output_path.joinpath(f'/sec{secondsCounter}/{real_frame_nr}.png'), frame)

        current_frame_nr += 1
        if real_frame_nr >= real_target_framerate:
            print(f'We are at second {secondsCounter} of {total_len_in_sec}')
            real_frame_nr = 0
            current_frame_nr = 0
            secondsCounter += 1
            Path(frames_output_path.joinpath(f'/sec{secondsCounter}')).mkdir(parents=True, exist_ok=True)
        cv2.waitKey(delay_time)
    
    video.release()

def merge_frames(frames_input_path, video_output_path):
    print(frames_input_path)
    print(os.listdir(frames_input_path))
    for second in os.listdir(frames_input_path):
        print(frames_input_path + '/')
        frames = [img for img in os.listdir(frames_input_path + '/' + second) if img.endswith(".png")]
        print(frames)

project_name = 'testproject'
dirname = os.path.dirname(__file__)
frames_output_path = Path(dirname).parent.absolute().joinpath('sd-input/' + project_name)
frames_input_path = Path(dirname).parent.absolute().joinpath('sd-output/' + project_name)
video_input_path = '/home/user/Code/vid2vid/samplevid.mp4'
video_output_path = '/home/user/Code/vid2vid/newsamplevid.mp4'
# can only be specified lower than the current framerate is
# conversion is also pretty bad/ simple and when not doing 60 to 30 or
# something the result will not be the desired framerate because of rounding issues
# with my simple conversion
desired_framerate = 15
Path(frames_output_path).mkdir(parents=True, exist_ok=True)
Path(frames_input_path).mkdir(parents=True, exist_ok=True)
split_video(video_input_path, frames_output_path, desired_framerate)
# merge_frames(frames_input_path, video_output_path)
