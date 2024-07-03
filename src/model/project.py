class Project:
    def __init__(self, id=None, user_id=None, title=None, script_id=None, images=None, audio_id=None, render_id=None, state=None, voiceovers=None):
        self.id : str = id
        self.user_id : str = user_id
        self.title : str  = title
        self.script_id : str = script_id
        self.images : list[str] = images or []
        self.audio_id : str = audio_id
        self.render_id : str = render_id
        self.state : str = state
        self.voiceovers : list[str] = voiceovers or []

    def to_json(self, include_id=True):
        result = {
            'user_id': self.user_id,
            'title': self.title,
            'script_id': self.script_id,
            'images': self.images,
            'music_id': self.audio_id,
            'render_id': self.render_id,
            'state': self.state,
            'voiceovers': self.voiceovers
        }
        if include_id:
            result['id'] = self.id
        return result

    def equals(self, other : 'Project') -> bool:
        return (self.id == other.id and
                self.user_id == other.user_id and
                self.title == other.title and
                self.script_id == other.script_id and
                self.images == other.images and
                self.audio_id == other.audio_id and
                self.render_id == other.render_id and
                self.state == other.state and
                self.voiceovers == other.voiceovers)

    def merge_projects(self, new_project : 'Project') -> 'Project':
        merged_project = Project(id=self.id, user_id=self.user_id, title=self.title, script_id=self.script_id, images=self.images, audio_id=self.audio_id, render_id=self.render_id, state=self.state, voiceovers=self.voiceovers)
        if new_project.title:
            merged_project.title = new_project.title

        if new_project.script_id:
            merged_project.script_id = new_project.script_id

        if new_project.images:
            merged_project.images = new_project.images

        if new_project.audio_id:
            merged_project.audio_id = new_project.audio_id

        if new_project.render_id:
            merged_project.render_id = new_project.render_id

        if new_project.state:
            merged_project.state = new_project.state    

        return merged_project
    
    @staticmethod
    def from_json(data) -> 'Project':
        return Project(id=str(data.get("_id")), 
                       user_id=data.get("user_id"), 
                       title=data.get("title"), 
                       script_id=data.get("script_id") if "script_id" in data else None, 
                       images=data.get("images") if "images" in data else [], 
                       audio_id=data.get("music_id") if "music_id" in data else None, 
                       render_id=data.get("render_id") if "render_id" in data else None, 
                       state=data.get("state"),
                       voiceovers=data.get("voiceovers") if "voiceovers" in data else [])
