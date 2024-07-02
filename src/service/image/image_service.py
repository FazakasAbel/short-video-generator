import requests
import os
import logging as log
from src.model.image_url import Image
from src.repo.image_repo import ImageUrlRepository
from src.service.image.dalle_service import DalleService
from src.api.exceptions.GenerationUnsuccessful import GenerationUnsuccessful
from src.api.exceptions.DocumentNotFound import DocumentNotFound
from src.api.exceptions.NoUpdateDone import NoUpdateDone
from io import BytesIO

class ImageService:

    def __init__(self):
        self.dalle_service = DalleService()
        self.image_repo = ImageUrlRepository()
    
    def save_image(self, url : str, duration : int) -> str:
        content = self.download_image(url)
        image = Image(file=content, duration=duration)
        image_id = self.image_repo.save_image(image)
        if not image_id:
            log.warn("Failed to save image")
            raise Exception

        log.info("Image saved successfully")
        return image_id

    def get_image(self, image_id : str) -> Image:
        image = self.image_repo.get_image(image_id)
        if not image:
            log.warn("Failed to get image")
            raise DocumentNotFound("Image not found")

        log.info("Image fetched successfully")
        return image

    def update_image(self, image_id : str, updated_data : Image) -> None:
        image = self.image_repo.get_image(image_id)
        if not image:
            log.warn("Failed to get image")
            raise DocumentNotFound

        merged_image : Image = image.merge_images(updated_data)
        if image.equals(merged_image):
            log.warn("No update done")
            raise NoUpdateDone

        self.image_repo.update_image(image_id, merged_image)

    def delete_image(self, image_id : str) -> None:
        deleted = self.image_repo.delete_image(image_id)
        
        if not deleted:
            log.warn("Failed to delete image")
            raise DocumentNotFound    

    def download_image(self, image_url : str) -> BytesIO:
        response = requests.get(image_url)
        if response.status_code != 200:
            log.warn("Failed to download image", response.status_code)
            raise Exception

        log.info("Image downloaded successfully")
        return BytesIO(response.content)
 
    def generate_dalle_image(self, prompt : str, size : str = "1024x1792", quality : str = "standard") -> Image:
        
        image_url = self.dalle_service.generate_dalle_image(prompt, size, quality)
        if not image_url:
            log.warn("Failed to generate image")
            raise GenerationUnsuccessful

        log.info("Image generated successfully")
        return image_url
        
