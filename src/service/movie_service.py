from sys import exit
from argparse import ArgumentParser
from os import listdir
from os.path import isfile, join
from cv2 import imread, VideoWriter_fourcc, VideoWriter, resize
from re import compile
from dataclasses import dataclass
from tqdm import tqdm
import cv2 as cv2
from moviepy.editor import ImageSequenceClip
import moviepy as mp
from src.service.image_service import ImageService
from src.model.image_url import ImageUrl
import numpy as np
import urllib.request
from io import BytesIO
from tempfile import NamedTemporaryFile

@dataclass
class MovieService:
    def __init__(self, fps: int, size: tuple, max_zoom: int):
        self.fps = fps
        self.size = size
        self.max_zoom = max_zoom
        self.image_service = ImageService()

    #def generate_slideshow(self, image_urls : list[ImageUrl]):
    #    codec = cv2.VideoWriter_fourcc(*'mp4v')
    #    out = cv2.VideoWriter(
    #        None,
    #        codec,
    #        float(self.fps),
    #        self.size,
    #    )
    #    video_frames = []
    #    for image_url in tqdm(image_urls, desc="Making"):
    #        url_response = urllib.request.urlopen(image_url.url)
    #        img = cv2.imdecode(np.array(bytearray(url_response.read()), dtype=np.uint8), -1)
    #        for i in range(int(image_url.duration * float(self.fps))):
    #            zoomed_img = zoom_at(img, zoom=1 + (i / (image_url.duration * float(self.fps))))
    #            zoomed_img = resize(zoomed_img, self.size)
    #            video_frames.append(zoomed_img)
    #    for frame in video_frames:
    #        out.write(frame)
    #    out.release()
    #    ret, buffer = cv2.imencode(
    #        '.mp4',
    #        out.get(1),
    #    )
    #    video_bytes = buffer.tobytes()
    #    return video_bytes

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
    

