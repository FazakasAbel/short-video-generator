class ImageDescription:
    def __init__(self, description, duration):
        self.description = description
        self.duration = duration

    def to_json(self): 
        return {
            'description': self.description,
            'duration': self.duration
        }   

    @staticmethod
    def from_json(data):
        return ImageDescription(description=data['description'], duration=data['duration'])
    
    def equals(self, other):
        return self.description == other.description and self.duration == other.duration