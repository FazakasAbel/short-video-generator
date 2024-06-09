import requests
import os
import logging as log
from src.model.image_url import ImageUrl
from src.repo.image_repo import ImageUrlRepository
from src.service.dalle_service import DalleService
from src.api.exceptions.GenerationUnsuccessful import GenerationUnsuccessful
from src.api.exceptions.DocumentNotFound import DocumentNotFound
from src.api.exceptions.NoUpdateDone import NoUpdateDone

class ImageService:

    def __init__(self):
        self.dalle_service = DalleService()
        self.image_repo = ImageUrlRepository()
    
    def save_image_url(self, image_url, duration):
        image_url = ImageUrl(url=image_url, duration=duration)
        image_id = self.image_repo.save_image_url(image_url)
        if not image_id:
            log.warn("Failed to save image")
            raise Exception

        log.info("Image saved successfully")
        return image_id

    def get_image_url(self, image_id):
        image_url = self.image_repo.get_image_url(image_id)
        if not image_url:
            log.warn("Failed to get image")
            raise DocumentNotFound("Image not found")

        log.info("Image fetched successfully")
        return image_url

    def update_image_url(self, image_id, updated_data : ImageUrl):
        image_url = self.image_repo.get_image_url(image_id)
        if not image_url:
            log.warn("Failed to get image")
            raise DocumentNotFound

        merged_image : ImageUrl = image_url.merge_images(updated_data)
        if image_url.equals(merged_image):
            log.warn("No update done")
            raise NoUpdateDone

        self.image_repo.update_image_url(image_id, merged_image)

    def delete_image_url(self, image_id):
        deleted = self.image_repo.delete_image_url(image_id)
        
        if not deleted:
            log.warn("Failed to delete image")
            raise DocumentNotFound    

    def download_image(self, image_url):
        response = requests.get(image_url)
        if response.status_code != 200:
            log.warn("Failed to download image", response.status_code)
            raise Exception

        log.info("Image downloaded successfully")
        return response.content
 
    def generate_dalle_image_url(self, prompt, size="1024x1792", quality="standard"):
        
        image_url = self.dalle_service.generate_dalle_image(prompt, size, quality)
        if not image_url:
            log.warn("Failed to generate image")
            raise GenerationUnsuccessful

        log.info("Image generated successfully")
        return image_url
        
