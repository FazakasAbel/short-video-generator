class SubsOptions:
    def __init__(self, emoji_animation: bool=True, emphasize_keywords: bool=True, animation: bool=True, punctuation: bool=True):
        self.emojiAnimation = emoji_animation
        self.emphasizeKeywords = emphasize_keywords
        self.animation = animation
        self.punctuation = punctuation

    def to_json(self):
        return {
            "emojiAnimation": self.emojiAnimation,
            "emphasizeKeywords": self.emphasizeKeywords,
            "animation": self.animation,
            "punctuation": self.punctuation
        }

   
    @staticmethod
    def from_json(data):
        return SubsOptions(
            emoji_animation=data.get("emojiAnimation", False),
            emphasize_keywords=data.get("emphasizeKeywords", False),
            animation=data.get("animation", False),
            punctuation=data.get("punctuation", False)
        )

