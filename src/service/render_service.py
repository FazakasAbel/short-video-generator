from src.repo.render_repo import RenderRepository
from src.api.exceptions.DocumentNotFound import DocumentNotFound
from src.model.render import Render

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

