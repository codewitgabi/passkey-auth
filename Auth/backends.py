from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class PasskeyAuthenticationBackend(BaseBackend):
    def authenticate(self, request, userId, email):
        try:
            user = User.objects.get(id=userId, email=email)
        except User.DoesNotExist:
            user = None

        return user
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

