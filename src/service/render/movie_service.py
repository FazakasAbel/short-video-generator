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
from src.model.image_url import Image
from src.model.audio import Audio
from src.model.render import Render
import numpy as np
import urllib.request
from io import BytesIO
from tempfile import NamedTemporaryFile
import logging
import moviepy.editor as mp
import math
from PIL import Image as PILImage

@dataclass
class MovieService:
    def __init__(self, fps: int, size: tuple, max_zoom: int):
        self.fps = fps
        self.size = size
        self.max_zoom = max_zoom
        self.image_service = ImageService()
        self.zoom_ratio = 0.04

    
    # Function to apply a zoom-in effect to a moviepy clip
    def zoom_in_effect(self, clip, zoom_ratio=0.04):
        """
        Applies a zoom-in effect to a moviepy clip.

        Args:
            clip (moviepy.Clip): The clip to which the zoom-in effect will be applied.
            zoom_ratio (float, optional): The zoom ratio. Defaults to 0.04.

        Returns:
            moviepy.Clip: The clip with the applied zoom-in effect.
        """
        # Define the effect function
        def effect(get_frame, t):
            # Get the frame at time t
            img = PILImage.fromarray(get_frame(t))
            base_size = img.size

            # Calculate the new size based on the zoom ratio
            new_size = [
                math.ceil(img.size[0] * (1 + (zoom_ratio * t))),
                math.ceil(img.size[1] * (1 + (zoom_ratio * t)))
            ]

            # Ensure the new dimensions are even
            new_size[0] = new_size[0] + (new_size[0] % 2)
            new_size[1] = new_size[1] + (new_size[1] % 2)

            # Resize the image
            img = img.resize(new_size)

            # Calculate the cropping coordinates
            x = math.ceil((new_size[0] - base_size[0]) / 2)
            y = math.ceil((new_size[1] - base_size[1]) / 2)

            # Crop and resize the image
            img = img.crop([
                x, y, new_size[0] - x, new_size[1] - y
            ]).resize(base_size)

            # Convert the image back to numpy array and close the image object
            result = np.array(img)
            img.close()

            return result

        # Apply the effect to the clip
        return clip.fl(effect)
    

    # Function to generate a slideshow video from a list of image URLs
    def generate_slideshow(self, images: list[Image]):
        """
        Generates a slideshow video from a list of image URLs.

        Args:
            image_urls (list[ImageUrl]): The list of image URLs.

        Returns:
            bytes: The generated slideshow video as bytes.
        """
        size = (1024, 1792)

        slides = []
        for n, image in enumerate(images):
            # Create a clip from the image URL
            #image_array = np.asarray(PILImage.open(image.file))
            
            with NamedTemporaryFile(suffix=".jpg") as temp_file:
                temp_filename = temp_file.name
                temp_file.write(image.file.read())
                slides.append(
                    mp.ImageClip(temp_filename).set_fps(self.fps).set_duration(image.duration)
                )


            #slides.append(
            #    mp.ImageClip(image_array).set_fps(self.fps).set_duration(image.duration)
            #)

            # Apply the zoom-in effect to the clip
            #slides[n] = self.zoom_in_effect(slides[n], 0.04)

        # Concatenate the slides into a video clip
        video = mp.concatenate_videoclips(slides)
        with NamedTemporaryFile(suffix=".avi") as temp_file:
            temp_filename = temp_file.name
            # Write the video clip to a temporary file
            video.write_videofile(temp_filename, codec='mpeg4', fps=float(self.fps), audio=False)
            temp_file.seek(0)
            # Read the temporary file as bytes
            video_bytes = temp_file.read()
        
        return video_bytes

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
        with NamedTemporaryFile(suffix=".avi") as temp_file:
            temp_filename = temp_file.name
            video_with_audio.write_videofile(temp_filename, codec='mpeg4', fps=float(self.fps))
            temp_file.seek(0)
            video_bytes = temp_file.read()
    
        return video_bytes

    def video_clip_from_bytes(self, render):
        with NamedTemporaryFile(suffix='.avi') as f:
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
