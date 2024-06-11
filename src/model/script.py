from dataclasses import dataclass
from src.model.scene import Scene

@dataclass
class Script:
    def __init__(self, id=None, theme=None, script : list[Scene] =None):
        self.id = id
        self.theme = theme
        self.script : list[Scene] = script or []

    def to_json(self, include_id=True):
        result = {
            'theme': self.theme,
            'script': [scene.to_json() for scene in self.script]
        }
        if include_id:
            result['_id'] = self.id
        return result

    def merge_scripts(self, new_script):
        merged_script : Script = Script(id=self.id, theme=self.theme, script=self.script)
        if new_script.theme:
            merged_script.theme = new_script.theme

        if new_script.script:
            merged_script.script = new_script.script

        return merged_script

    def equals(self, other):
        return (self.id == other.id and
                self.theme == other.theme and
                len(self.script) == len(other.script) and
                all(map(lambda pair: pair[0].equals(pair[1]), zip(self.script, other.script))))
    
    def get_image_descriptions(self):
        return [image_description for scene in self.script for image_description in scene.images]
  
    @staticmethod
    def from_json(data):
        return Script(id=str(data['_id']), theme=data['theme'], script=[Scene.from_json(scene) for scene in data['script']])

    def get_text_descriptions(self):
        return [scene.text for scene in self.script]
    
    def get_voiceover_durations(self):
        return map(lambda scene: sum(map(lambda image_description: image_description.duration, scene.images)), self.script)