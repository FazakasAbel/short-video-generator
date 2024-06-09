from src.model.image_description import ImageDescription
import logging as log

class Scene:
    def __init__(self, imageDescriptions : list[ImageDescription]=None, text=None):
        self.images : list[ImageDescription] = imageDescriptions or []
        self.text = text

    def to_json(self):
        return {
            'images': [image.to_json() for image in self.images],
            'text': self.text
        }
    
    @staticmethod
    def from_json(data):
        log.exception(data)
        return Scene(imageDescriptions=[ImageDescription.from_json(image) for image in data['images']], text=data['text'])
    
    def equals(self, other):
        return (self.text == other.text and 
                len(self.images) == len(other.images)
                and all(map(lambda pair: pair[0].equals(pair[1]), zip(self.images, other.images))))
