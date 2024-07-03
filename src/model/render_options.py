from src.model.highlight_options import HighlightOptions
from src.model.style_options import StyleOptions
from src.model.subs_options import SubsOptions

class RenderOptions:
    def __init__(self, subs_options: SubsOptions = SubsOptions(), style_options: StyleOptions = StyleOptions(), highlight_options: HighlightOptions = HighlightOptions()):
        self.subs_options = subs_options
        self.style_options = style_options
        self.highlight_options = highlight_options

    def to_json(self):
        return {
            "subsOptions": self.subs_options.to_json(),
            "styleOptions": self.style_options.to_json(),
            "highlightOptions": self.highlight_options.to_json()
        }

    @staticmethod
    def from_json(data):
        return RenderOptions(
            subs_options=SubsOptions.from_json(data["subsOptions"]),
            style_options=StyleOptions.from_json(data["styleOptions"]),
            highlight_options=HighlightOptions.from_json(data["highlightOptions"]))