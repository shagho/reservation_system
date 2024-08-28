from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    def create_user(self, username, name, password):
        if not username:
            raise ValueError("The given username must be set")
        if not name:
            raise ValueError("The given name must be set")
        
        user = self.model(username=username, name=name)
        user.password = make_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, name, password=None):
        user = self.create_user(username, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user