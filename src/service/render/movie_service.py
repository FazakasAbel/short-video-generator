from sys import exit
from argparse import ArgumentParser
from os import listdir
from os.path import isfile, join
from cv2 import imread, VideoWriter_fourcc, VideoWriter, resize
from re import compile
from dataclasses import dataclass
from tqdm import tqdm
import cv2 as cv2
from moviepy.editor import ImageSequenceClip, AudioFileClip, VideoFileClip, CompositeAudioClip
from src.service.image.image_service import ImageService
from src.model.image_url import ImageUrl
from src.model.audio import Audio
from src.model.render import Render
import numpy as np
import urllib.request
from io import BytesIO
from tempfile import NamedTemporaryFile
import logging

@dataclass
class MovieService:
    def __init__(self, fps: int, size: tuple, max_zoom: int):
        self.fps = fps
        self.size = size
        self.max_zoom = max_zoom
        self.image_service = ImageService()

    def generate_slideshow(self, image_urls: list[ImageUrl]):
        video_frames = []
        
        # Generate video frames
        for image_url in tqdm(image_urls, desc="Making"):
            url_response = urllib.request.urlopen(image_url.url)
            img = cv2.imdecode(np.array(bytearray(url_response.read()), dtype=np.uint8), -1)
            for i in range(int(image_url.duration * float(self.fps))):
                zoomed_img = self.zoom_at(img, zoom=1 + (i / (image_url.duration * float(self.fps))))
                zoomed_img = resize(zoomed_img, self.size)
                video_frames.append(zoomed_img)
        
        # Create a video clip from the frames
        clip = ImageSequenceClip(video_frames, fps=float(self.fps))
        
        # Write video to a byte stream
        with NamedTemporaryFile(suffix=".mp4") as temp_file:
            temp_filename = temp_file.name
            clip.write_videofile(temp_filename, codec='mpeg4', fps=float(self.fps), audio=False)
            temp_file.seek(0)
            video_bytes = temp_file.read()
        
        return video_bytes
        
        # Return video bytes
        return video_buffer.read()
    
    def zoom_at(self, img, zoom=1, angle=0, coord=None):
        cy, cx = [i / 2 for i in img.shape[:-1]] if coord is None else coord[::-1]
        rot_mat = cv2.getRotationMatrix2D((cx, cy), angle, zoom)
        result = cv2.warpAffine(img, rot_mat, img.shape[1::-1], flags=cv2.INTER_LINEAR)
        return result
    

    def add_narration_to_video(self, render : Render, audios : list[tuple[Audio, int]]):
        video_clip = self.video_clip_from_bytes(render.file)

         # Create a list to hold the intervals at which additional audio clips will play
        intervals = []
        current_time = 0
        # Load additional audios and schedule them according to their durations
        for audio, duration in audios:
            additional_clip = self.audio_clip_from_bytes(audio.file)
            sped_up_clip = additional_clip
            logging.exception("added audio clip at time: " + str(current_time))
            intervals.append((sped_up_clip, current_time))    
            current_time = current_time + duration

        # Create a list of the audio clips to be combined
        audio_clips = []
    
        # Add the additional audio clips at their respective start times
        for clip, start in intervals:
            audio_clips.append(clip.set_start(start))
    
        # Combine all the audio clips into a single audio track
        combined_audio = CompositeAudioClip(audio_clips)
        video_with_audio = video_clip.set_audio(combined_audio)
        with NamedTemporaryFile(suffix=".mp4") as temp_file:
            temp_filename = temp_file.name
            video_with_audio.write_videofile(temp_filename, codec='mpeg4', fps=float(self.fps))
            temp_file.seek(0)
            video_bytes = temp_file.read()
    
        return video_bytes

    def video_clip_from_bytes(self, render):
        with NamedTemporaryFile(suffix='.mp4') as f:
            f.write(render.read())
            f.flush()
            video_clip = VideoFileClip(f.name)
        return video_clip
    
    def audio_clip_from_bytes(self, audio):
        with NamedTemporaryFile(suffix='.mp3') as f:
            f.write(audio.read())
            f.flush()
            audio_clip = AudioFileClip(f.name)
        return audio_clip
