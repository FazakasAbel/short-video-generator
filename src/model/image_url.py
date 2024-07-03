from io import BytesIO

class Image:

    def __init__(self, id : str =None, file : BytesIO =None, duration : int =None):
        self.id : str = id
        self.file : BytesIO = file
        self.duration : int = duration

    def to_json(self, include_id : bool =True):
        result = {
            'file': self.file.getvalue(),
            'duration': self.duration
        }
        if include_id:
            result['_id'] = self.id
        return result
    
    @staticmethod
    def from_json(data) -> 'Image':
        return Image(id=str(data['_id']), file=BytesIO(data['file']), duration=data['duration'])
    
    def equals(self, other : 'Image'):
        return (self.file == other.file and
                self.duration == other.duration)
    
    def merge_image_url(self, new_image : 'Image') -> 'Image':
        merged_image = Image(id=self.id, file=self.file, duration=self.duration)

        if new_image.duration:
            merged_image.duration = new_image.duration

        if new_image.file:
            merged_image.file = new_image.file

        return merged_image
    
