
class ImageUrl:

    def __init__(self, id=None, url=None, duration=None):
        self.id = id
        self.url = url
        self.duration = duration

    def to_json(self, include_id=True):
        result = {
            'url': self.url,
            'duration': self.duration
        }
        if include_id:
            result['_id'] = self.id
        return result
    
    @staticmethod
    def from_json(data):
        return ImageUrl(id=str(data['_id']), url=data['url'], duration=data['duration'])
    
    def equals(self, other):
        return (self.url == other.url and
                self.duration == other.duration)
    
    def merge_image_url(self, new_image_url):
        merged_image_url = ImageUrl(id=self.id, url=self.url, duration=self.duration)

        if new_image_url.duration:
            merged_image_url.duration = new_image_url.duration

        if new_image_url.url:
            merged_image_url.url = new_image_url.url

        return merged_image_url
    
