class HighlightOptions:
    def __init__(self, random_colour_one="#2bf82a", random_colour_two="#fdfa14", random_colour_three="#f01916"):
        self.random_colour_one = random_colour_one
        self.random_colour_two = random_colour_two
        self.random_colour_three = random_colour_three

    def from_json(data):
        return HighlightOptions(
            random_colour_one=data.get("randomColourOne", "#2bf82a"),
            random_colour_two=data.get("randomColourTwo", "#fdfa14"),
            random_colour_three=data.get("randomColourThree", "#f01916")
        )
    
    def to_json(self):
        return {
            "randomColourOne": self.random_colour_one,
            "randomColourTwo": self.random_colour_two,
            "randomColourThree": self.random_colour_three
        }
