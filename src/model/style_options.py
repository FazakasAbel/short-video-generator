from dataclasses import dataclass

@dataclass
class StyleOptions:

    def __init__(self, top: int=40, font_uppercase: bool=True, font_size: int=46, font_weight: int=900, font_color: str="#ffffff"):
        self.top = top
        self.font_uppercase = font_uppercase
        self.font_size = font_size
        self.font_weight = font_weight
        self.font_color = font_color
    
    @staticmethod
    def from_json(data):
        return StyleOptions(
            top=data.get("top", 40),
            font_uppercase=data.get("fontUppercase", True),
            font_size=data.get("fontSize", 46),
            font_weight=data.get("fontWeight", 900),
            font_color=data.get("fontColor", "#ffffff")
        )
    
    def to_json(self):
        return {
            "top": self.top,
            "fontUppercase": self.font_uppercase,
            "fontSize": self.font_size,
            "fontWeight": self.font_weight,
            "fontColor": self.font_color
        }