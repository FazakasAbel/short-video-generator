from src.repo.project_repo import ProjectRepository
from src.api.exceptions.DocumentNotFound import DocumentNotFound
from src.api.exceptions.NoUpdateDone import NoUpdateDone 
from src.api.exceptions.GenerationUnsuccessful import GenerationUnsuccessful
from src.model.image_description import ImageDescription
from src.service.image_service import ImageService
from src.service.script_service import ScriptService
from src.model.script import Script
from src.model.project import Project
from src.model.image_url import ImageUrl
from src.service.movie_service import MovieService
from src.service.render_service import RenderService
import logging

class ProjectService:
    def __init__(self):
        self.repo = ProjectRepository()
        self.image_service = ImageService()
        self.script_service = ScriptService()
        self.movie_service = MovieService(30, (1024, 1792), 2)
        self.render_service = RenderService()

    def save_project(self, user_id, title,  state, script_id=None, images=None, audio_id=None, render_id=None):
        project = Project(user_id=user_id, title=title, script_id=script_id, images=images, audio_id=audio_id, render_id=render_id, state=state)
        return self.repo.save_project(project)

    def get_project(self, project_id):
        project = self.repo.get_project(project_id)
        if not project:
            raise DocumentNotFound
        
        return project

    def update_project(self, project_id, updated_data : Project):
        project : Project = self.repo.get_project(project_id)
        if not project:
            raise DocumentNotFound

        merged_project : Project = project.merge_projects(updated_data)
        if project.equals(merged_project):
            raise NoUpdateDone

        self.repo.update_project(project_id, merged_project)
        updated_project = self.repo.get_project(project_id)
        return updated_project

    def delete_project(self, project_id):
        #TODO - refactor delete methods to use deleted_count 
        project = self.repo.get_project(project_id)
        if not project:
            raise DocumentNotFound

        self.repo.delete_project(project_id)

    def get_projects_by_user_id(self, user_id):
        projects = self.repo.get_projects_by_user_id(user_id)
        return projects    
    

    def update_project_state(self, project_id, state):
        project = self.repo.get_project(project_id)
        if not project:
            raise DocumentNotFound

        if project.state == state:
            raise NoUpdateDone

        project.state = state
        self.repo.update_project(project_id, project)
        updated_project = self.repo.get_project(project_id)

        return updated_project
    
    def generate_images(self, project_id):
        project : Project = self.repo.get_project(project_id)
        if not project:
            raise DocumentNotFound("Project not found")

        script_id = project.script_id
        if not script_id:
            raise NoUpdateDone

        script : Script = self.script_service.get_script(script_id)
        if not script:
            raise DocumentNotFound("Script not found")

        image_descriptions : list[ImageDescription] = script.get_image_descriptions()

        images_urls = [ImageUrl(url=self.image_service.generate_dalle_image_url(image_description.description), duration=image_description.duration) for image_description in image_descriptions]
        image_ids = []
        for image_url in images_urls:
            image_id = self.image_service.save_image_url(image_url.url, image_url.duration)
            if not image_id:
                raise GenerationUnsuccessful("Failed to save image")
            image_ids.append(image_id)
            
        self.update_project_images(project_id, image_ids)
        return image_ids

    def update_project_images(self, project_id, images_ids):
        self.repo.update_project_images(project_id, images_ids)       

    def generate_script(self, project_id, theme):
        scene_list = self.script_service.generate_script(theme)

        if not scene_list:
            raise GenerationUnsuccessful("Failed to generate script")
        script_id = self.script_service.save_script(Script(theme=theme, script=scene_list))

        if not script_id:
            raise GenerationUnsuccessful("Failed to save script")

        self.update_project_script(project_id, script_id)
        return script_id

    def update_project_script(self, project_id, script_id):
        self.repo.update_project_script(project_id, script_id)

    def update_project_render(self, project_id, render_id):
        self.repo.update_project_render(project_id, render_id)  

    def generate_project_slideshow(self, project_id): 
        project = self.get_project(project_id)
        if not project:
            raise DocumentNotFound("Project not found")
        
        image_ids = project.images
        if not image_ids or len(image_ids) == 0:
            raise DocumentNotFound(f"Images missing in project {project_id}")
        
        image_urls = [self.image_service.get_image_url(image_id) for image_id in image_ids]
        if not image_urls or len(image_urls) == 0:
            raise DocumentNotFound("Images not found")
        
        slideshow = self.movie_service.generate_slideshow(image_urls)
        if not slideshow:
            raise GenerationUnsuccessful("Failed to generate slideshow")

        render_id = self.render_service.save_render(slideshow, f"{project.id}_slideshow.mp4")

        if not render_id:
            raise GenerationUnsuccessful("Failed to save render")

        self.update_project_render(project_id, render_id)
        return render_id