from .models import *
from django.db.models import Q

class AuthBackend(object):
    supports_object_permissions = True
    supports_anonymous_user = False
    supports_inactive_user = False


    def get_user(self, user_id):
       try:
          return User.objects.get(pk=user_id)
       except User.DoesNotExist:
          return None


    def authenticate(self, email, password, is_staff, is_active):
        try:
            user = User.objects.get(
               Q(email=email) | Q(phone_number=email), is_staff=is_staff, is_active=1
            )
        except User.DoesNotExist:
            return None

        return user if user.check_password(password) else None
