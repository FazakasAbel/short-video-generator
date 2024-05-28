from dataclasses import dataclass
from typing import List

@dataclass
class Project:
    user_id: str
    theme: str
    state: str
    script_id: str
    images: List[str]
    music_id: str
    render_id: str
