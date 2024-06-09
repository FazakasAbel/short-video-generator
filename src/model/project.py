class Project:
    def __init__(self, id=None, user_id=None, title=None, script_id=None, images=None, audio_id=None, render_id=None, state=None):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.script_id = script_id
        self.images = images or []
        self.audio_id = audio_id
        self.render_id = render_id
        self.state = state

    def to_json(self, include_id=True):
        result = {
            'user_id': self.user_id,
            'title': self.title,
            'script_id': self.script_id,
            'images': self.images,
            'audio_id': self.audio_id,
            'render_id': self.render_id,
            'state': self.state
        }
        if include_id:
            result['id'] = self.id
        return result

    def equals(self, other):
        return (self.id == other.id and
                self.user_id == other.user_id and
                self.title == other.title and
                self.script_id == other.script_id and
                self.images == other.images and
                self.audio_id == other.audio_id and
                self.render_id == other.render_id and
                self.state == other.state)

    def merge_projects(self, new_project):
        merged_project = Project(id=self.id, user_id=self.user_id, title=self.title, script_id=self.script_id, images=self.images, audio_id=self.audio_id, render_id=self.render_id, state=self.state)
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