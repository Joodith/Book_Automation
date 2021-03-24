from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

user_model=settings.AUTH_USER_MODEL

class EmailOrUsernameModelBackend(object):
    def authenticate(self,username=None,password=None):
        if '@' in username:
            kwargs={'email':username}
        else:
            kwargs={'username':username}
        try:
            user=get_user_model().objects.get(**kwargs)
            if user.check_password(password):
                return user
        except:
            return None

    def authenticate_only_username(self,username=None):
        if '@' in username:
            kwargs={'email':username}
        else:
            kwargs={'username':username}
        try:
            user=get_user_model().objects.get(**kwargs)
            return user
        except:
            return None

    def get_user(self, username):
        try:
            return get_user_model().objects.get(pk=username)
        except get_user_model().DoesNotExist:
            return None
