from src.repo.render_repo import RenderRepository
from src.api.exceptions.DocumentNotFound import DocumentNotFound
from src.model.render import Render
import requests

class RenderService:
    def __init__(self):
        self.repo = RenderRepository()

    def save_render(self, file, filename):
        render = Render(file=file, filename=filename)
        return self.repo.save_render(render)

    def get_render(self, render_id):
        render = self.repo.get_render(render_id)
        if not render:
            raise DocumentNotFound
        
        return render

    def delete_render(self, render_id):
        render = self.repo.get_render(render_id)
        if not render:
            raise DocumentNotFound
        
        self.repo.delete_render(render_id)

    @staticmethod
    def download_video(url):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            # Collect the video content as bytes
            video_bytes = b""
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    video_bytes += chunk

            return video_bytes

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while downloading the video: {e}")
            return None

