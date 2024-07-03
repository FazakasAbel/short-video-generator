from dataclasses import dataclass
from typing import List

@dataclass
class User:
    id: str
    username: str
    email: str
    project_ids: List[str]

    def __init__(self, id=None, username=None, email=None, project_ids=None):
        self.id = id
        self.username = username
        self.email = email
        self.project_ids = project_ids or []        
    
    def to_json(self, include_id=True):
        result = {
            'username': self.username,
            'email': self.email,
            'project_ids': self.project_ids
        }
        if include_id:
            result['id'] = self.id
        return result
    def merge_users(self, new_user):
        merged_user : User = User(id=self.id, username=self.username, email=self.email, project_ids=self.project_ids)
        if new_user.username:
            merged_user.username = new_user.username

        if new_user.email:
            merged_user.email = new_user.email

        if new_user.project_ids:
            merged_user.project_ids = new_user.project_ids

        return merged_user

    def equals(this, other):
        return (this.id == other.id and 
                this.username == other.username and 
                this.email == other.email and 
                this.project_ids == other.project_ids)    

    
    
