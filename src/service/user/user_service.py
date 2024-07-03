from src.repo.user_repo import UserRepository
from src.api.exceptions.DocumentNotFound import DocumentNotFound
from src.api.exceptions.NoUpdateDone import NoUpdateDone 
from src.model.user import User
import logging

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def save_user(self, username, email): 
        user = User(username=username, email=email)
        return self.repo.save_user(user)

    def get_user(self, user_id):
        user = self.repo.get_user(user_id)
        if not user:
            raise DocumentNotFound
        
        return user

    def update_user(self, user_id, updated_data : User):
        user : User = self.repo.get_user(user_id)
        if not user:
            raise DocumentNotFound

        merged_data : User = user.merge_users(updated_data)
        if user.equals(user):
            raise NoUpdateDone

        self.repo.update_user(user_id, merged_data)
        updated_user = self.repo.get_user(user_id)
        return updated_user

    def delete_user(self, user_id):
        user = self.repo.get_user(user_id)
        if not user:
            raise DocumentNotFound

        self.repo.delete_user(user_id)
