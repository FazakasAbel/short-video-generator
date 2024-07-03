class Render:
    def __init__(self, id=None, file=None, filename=None):
        self.id = id
        self.file = file
        self.filename = filename

    def to_json(self, include_id=True):
        result = {
            'file': self.file,
            'filename': self.filename
        }
        if include_id:
            result['id'] = self.id
        return result
    
    def equals(self, other):
        return (self.file == other.file and
                self.filename == other.filename)
    
    def merge_renders(self, new_render):
        merged_render = Render(self.file, self.filename)
        if new_render.filename:
            merged_render.filename = new_render.filename

        return merged_render