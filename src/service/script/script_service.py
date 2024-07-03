from src.repo.script_repo import ScriptRepository
from src.api.exceptions.DocumentNotFound import DocumentNotFound
from src.api.exceptions.NoUpdateDone import NoUpdateDone 
from src.model.script import Script
import logging
from src.service.script.script_generator import YouTubeScriptGenerator 


class ScriptService:
    def __init__(self):
        self.repo = ScriptRepository()
        self.yt_script_generator = YouTubeScriptGenerator()

    def save_script(self, script):
        return self.repo.save_script(script)

    def get_script(self, script_id):
        script = self.repo.get_script(script_id)
        if not script:
            raise DocumentNotFound

        return script

    def update_script(self, script_id, updated_data: Script):
        script = self.repo.get_script(script_id)
        if not script:
            raise DocumentNotFound

        merged_data: Script = script.merge_scripts(updated_data)
        if script.equals(merged_data):
            raise NoUpdateDone

        self.repo.update_script(script_id, merged_data)
        updated_script = self.repo.get_script(script_id)
        return updated_script

    def delete_script(self, script_id):
        deleted = self.repo.delete_script(script_id)
        if not deleted:
            raise DocumentNotFound
        
    def generate_script(self, theme):
        return self.yt_script_generator.get_script(theme)

            
