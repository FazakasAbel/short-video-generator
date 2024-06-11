class Audio:
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
    
    def merge_audios(self, new_audio):
        merged_audio = Audio(self.id, self.file, self.filename)
        if new_audio.filename:
            merged_audio.filename = new_audio.filename

        return merged_audio