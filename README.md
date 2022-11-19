# Stable diffusion video modifier

## What 
This is a wrapper arround ![neonsecrets modified stable diffusion model](https://github.com/neonsecret/stable-diffusion). It allows lower end hardware users <8 GB VRAM to utilize stable diffusion without having to upgrade their rig. The script i added allows you to take a video file and perform a stable diffusion image operation on every frame. Because of performance reasons there is also the functionality to lower the fps of the video, as you might not want to wait for multiple days to render your 3 minute 60 fps video. 

## How
I have switched out the existing gradio user interface for a simple rest api to interact with the stable diffusion model. This implementation is found in the dockerized version of the model. I prefer to use the dockerized version as i had difficulties installing the prequesites for the bare bone one, and i suspect others might encounter the same issues. The video_altering script takes the input video, seperates it frame by frame, lowers the framerate on request and modifies them via the rest api. After that the resulting images are reconstructed into a video. Currently the audio of the video is lost.

## Prequesites

- python3 (tested with 3.10.6)
- pip install opencv-python
- docker + compose

## How to use

- only tested on linux so far
- create the folders specified in the docker-compose file in the parent of the clone of this repository. ('../sd-data', '../sd-output', '../sd-input')
This is necessary to do beforehand, because as docker would create them as root. After that they would not be accessible without changing the ownership/ permissions.
- get the pretrained stable diffusion weights from huggingfaces like described in the (official stable diffusion repo)[https://github.com/CompVis/stable-diffusion#:~:text=The%20weights%20are%20available] and place (or symlink) them in the '../sd-data' directory. The name of the model needs to be 'model.ckpt'
- launch the docker compose yml with 'docker compose up --build'. After it has compiled for the first time you only need to call 'docker compose up'
- launch the video altering script with the following params
'python video_altering.py PROJECT_NAME ABSOLUTE_VIDEO_INPUT_PATH ABSOLUTE_VIDEO_OUTPUT_PATH "PROMPT"
PROJECT_NAME = arbitrary name for folder structures e.g.: 'testproject'
ABSOLUTE_VIDEO_INPUT_PATH, ABSOLUTE_VIDEO_OUTPUT_PATH = absolute path to video in/output e.g.: '/home/user/Code/vid2vid/samplevid.mp4'
PROMPT = the prompt to alter the frames with e.g.: '"oil painting style"'

e.g.:
''

For more settings (like FPS adjustments, image size and so on) check out the parameterization at the end of the video_altering file.

## ToDo
- Port over the audio of the video