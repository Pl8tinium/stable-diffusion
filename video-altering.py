import cv2
from pathlib import Path
import math
import os
import re

def calc_real_framerate_info(current_framerate, desired_framerate, framerate_up_rounding=True):
    rounding_method = math.ceil if framerate_up_rounding else math.floor
    frame_skip = rounding_method(current_framerate / desired_framerate)
    real_target_framerate = rounding_method(current_framerate / frame_skip)
    return real_target_framerate, frame_skip

def get_delay_time(framerate):
    return int(1000 / framerate)

def get_framerate_info(video):
    current_framerate = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    return current_framerate, total_frames

def split_video(video, frames_output_path, desired_framerate, framerate_up_rounding=True):
    current_framerate, total_frames = get_framerate_info(video)
    total_len_in_sec = (total_frames / current_framerate) % 60
    real_target_framerate, frame_skip = calc_real_framerate_info(current_framerate, desired_framerate)
    print(f'current framerate{current_framerate} | desired framerate {desired_framerate} | actual framerate {real_target_framerate}')
    delay_time=get_delay_time(real_target_framerate)
    secondsCounter = 0
    current_frame_nr = 0
    real_frame_nr = 0
    Path(frames_output_path.joinpath(f'sec{secondsCounter}')).mkdir(parents=True, exist_ok=True)

    while (True):
        success, frame = video.read()
        if not success:
            print("finished! (or error)")
            break
        if (current_frame_nr % frame_skip) == 0:
            real_frame_nr += 1
            cv2.imwrite(str(frames_output_path.joinpath(f'sec{secondsCounter}/{real_frame_nr}.png')), frame)

        current_frame_nr += 1
        if real_frame_nr >= real_target_framerate:
            print(f'We are at second {secondsCounter} of {total_len_in_sec}')
            real_frame_nr = 0
            current_frame_nr = 0
            secondsCounter += 1
            Path(frames_output_path.joinpath(f'sec{secondsCounter}')).mkdir(parents=True, exist_ok=True)
        cv2.waitKey(delay_time)
    
    video.release()

def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower()
            for text in _nsre.split(s)]

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

def merge_frames(video, frames_input_path, video_output_path):
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    initialized = False

    for second in natural_sort(os.listdir(frames_input_path)):
        current_second_dir = frames_input_path.joinpath(f'{second}')
        frames = natural_sort([img for img in os.listdir(current_second_dir) if img.endswith(".png")])

        single_frame = cv2.imread(os.path.join(current_second_dir, frames[0]))
        if not initialized:
            initialized = True
            height, width, layers = single_frame.shape
            video = cv2.VideoWriter(video_output_path, fourcc, len(frames), (width,height))

        for frame in frames:
            video.write(cv2.imread(os.path.join(current_second_dir, frame)))

    cv2.destroyAllWindows()
    video.release()

project_name = 'testproject'
dirname = os.path.dirname(__file__)
frames_output_path = Path(dirname).parent.absolute().joinpath('sd-input/' + project_name)
frames_input_path = Path(dirname).parent.absolute().joinpath('sd-output/' + project_name)
video_input_path = '/home/user/Code/vid2vid/samplevid.mp4'
video_output_path = '/home/user/Code/vid2vid/newsamplevid.mp4'
# can only be specified lower than the current framerate is
# conversion is also pretty bad/ simple and when not doing 60 to 30 or
# something the result will not be the desired framerate because of rounding issues
# with my simple conversion, change the framerate_up_rounding param to use down round 
desired_framerate = 15
Path(frames_output_path).mkdir(parents=True, exist_ok=True)
Path(frames_input_path).mkdir(parents=True, exist_ok=True)
video = cv2.VideoCapture(video_input_path)
split_video(video, frames_output_path, desired_framerate)
merge_frames(video, frames_input_path, video_output_path)
