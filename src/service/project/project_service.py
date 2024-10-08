from src.repo.project_repo import ProjectRepository
from src.api.exceptions.DocumentNotFound import DocumentNotFound
from src.api.exceptions.NoUpdateDone import NoUpdateDone 
from src.api.exceptions.GenerationUnsuccessful import GenerationUnsuccessful
from src.model.image_description import ImageDescription
from src.service.image.image_service import ImageService
from src.service.script.script_service import ScriptService
from src.model.script import Script
from src.model.project import Project
from src.model.image_url import Image
from service.render.movie_service import MovieService
from service.render.render_service import RenderService
from src.service.audio.audio_service import AudioService
from src.service.render.zap_cap_service import ZapCapService
from src.model.render_options import RenderOptions
from io import BytesIO
import time
import logging
import json

class ProjectService:
    def __init__(self):
        self.repo = ProjectRepository()
        self.image_service = ImageService()
        self.script_service = ScriptService()
        self.movie_service = MovieService(30, (1024, 1792), 2)
        self.render_service = RenderService()
        self.audio_service = AudioService()
        self.zap_cap_service = ZapCapService()

    def save_project(self, user_id, title,  state, script_id=None, images=None, audio_id=None, render_id=None):
        project = Project(user_id=user_id, title=title, script_id=script_id, images=images, audio_id=audio_id, render_id=render_id, state=state)
        return self.repo.save_project(project)

    def get_projects(self) -> list[Project]:
        projects = self.repo.get_projects()
        if not projects:
            raise DocumentNotFound

        return projects

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
    
    def generate_images(self, project_id) -> list[str]:
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

        #TODO use zip
        images = [Image(file=self.image_service.generate_dalle_image(image_description.description), duration=image_description.duration) for image_description in image_descriptions]
        image_ids : list[str] = []
        for image in images:
            image_id = self.image_service.save_image(image.file, image.duration)
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
        
        image = [self.image_service.get_image(image_id) for image_id in image_ids]
        if not image or len(image) == 0:
            raise DocumentNotFound("Images not found")
        
        slideshow = self.movie_service.generate_slideshow(image)
        if not slideshow:
            raise GenerationUnsuccessful("Failed to generate slideshow")

        render_id = self.render_service.save_render(slideshow, f"{project.id}_slideshow.mp4")

        if not render_id:
            raise GenerationUnsuccessful("Failed to save render")

        self.update_project_render(project_id, render_id)
        return render_id
    
    def generate_project_voiceovers(self, project_id):
        project : Project = self.repo.get_project(project_id)
        if not project:
            raise DocumentNotFound("Project not found")

        script_id = project.script_id
        if not script_id:
            raise NoUpdateDone

        script : Script = self.script_service.get_script(script_id)
        if not script:
            raise DocumentNotFound("Script not found")
        
        texts = script.get_text_descriptions()
        if not texts or len(texts) == 0:
            raise DocumentNotFound("Texts not found")
        for text in texts:
            logging.exception(text)
        voiceovers = [self.audio_service.generate_voiceover(text) for text in texts]
        if not voiceovers:
            raise GenerationUnsuccessful("Failed to generate voiceovers")

        voiceover_ids = [self.audio_service.save_audio(file=voiceover, filename=f"{i}_voiceover") for i, voiceover in enumerate(voiceovers)]

        if not voiceover_ids:
            raise GenerationUnsuccessful("Failed to save voiceovers")

        self.update_project_voiceovers(project_id, voiceover_ids)
        return voiceover_ids
    
    def update_project_voiceovers(self, project_id, voiceover_ids):
        self.repo.update_project_voiceovers(project_id, voiceover_ids) 

    def generate_project_narration(self, project_id):
        project = self.repo.get_project(project_id)
        if not project:
            raise DocumentNotFound("Project not found")

        voiceovers = project.voiceovers
        if not voiceovers:
            raise NoUpdateDone

        voiceovers = [self.audio_service.get_audio(voiceover_id) for voiceover_id in voiceovers]
        if not voiceovers:
            raise DocumentNotFound("Voiceover not found")

        render = self.render_service.get_render(project.render_id)
        if not render:
            raise DocumentNotFound("Render not found")
        
        script = self.script_service.get_script(project.script_id)
        if not script:
            raise DocumentNotFound("Script not found")

        audios = zip(voiceovers, script.get_voiceover_durations())
        narration = self.movie_service.add_narration_to_video(render, audios)
        if not narration:
            raise GenerationUnsuccessful("Failed to generate narration")

        render_id = self.render_service.save_render(narration, f"{project.id}_narration.mp4")
        if not render_id:
            raise GenerationUnsuccessful("Failed to save render")

        self.update_project_render(project_id, render_id)
        return render_id
    
    def generate_project_subtitles(self, project_id): 

        project = self.repo.get_project(project_id)
        if not project:
            raise DocumentNotFound("Project not found")

        render = self.render_service.get_render(project.render_id)   
        if not render:
            raise DocumentNotFound("Render not found")

        video_upload_res = self.zap_cap_service.upload_video(render.file)
        if not video_upload_res:
            raise GenerationUnsuccessful("Failed to upload video")

        video_id = json.loads(video_upload_res)["id"]
        if not video_id:
            raise GenerationUnsuccessful("Failed to get video id")
        logging.exception(video_id)

        template_id = "cfa6a20f-cacc-4fb6-b1d0-464a81fed6cf"
        create_task_res = self.zap_cap_service.create_video_task(video_id, template_id=template_id, auto_approve=True, language="en", render_options=RenderOptions())
        
        if not create_task_res:
            raise GenerationUnsuccessful("Failed to create video task")

        task_id = json.loads(create_task_res)["taskId"]
        if not task_id:
            raise GenerationUnsuccessful("Failed to get task id")
        logging.exception(task_id)
        url=None
        done_try = 0
        max_try = 6
        while url==None and done_try<=max_try:
            get_task_res = self.zap_cap_service.get_video_task(video_id, task_id)
            if not get_task_res:
                raise GenerationUnsuccessful("Failed to get video task")
            done_try += 1
            url = json.loads(get_task_res)["downloadUrl"]
            logging.exception("going to sleep for 20s")
            time.sleep(20)

        #    if not url:
        #        raise GenerationUnsuccessful("Failed to get url")
        logging.exception(url)

        video = self.render_service.download_video(url)
        render_id = self.render_service.save_render(video, f"{project.title}_with_subtitles.mp4")
        if not render_id:
            raise GenerationUnsuccessful("Failed to save render")

        self.update_project_render(project_id, render_id)
        return render_id