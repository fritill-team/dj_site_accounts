from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()


class MultipleAuthenticationBackend(ModelBackend):
    def authenticate(self, request, *args, **kwargs):
        identifier = kwargs.pop('identifier', None)
        password = kwargs.pop('password', None)

        if not password or not identifier:
            return

        query = UserModel.objects.none()
        try:
            for field in UserModel.AUTHENTICATION_FIELDS:
                query = query | UserModel.objects.filter(**{field: identifier})
        except Exception as e:
            pass
        finally:
            if not query.exists():
                return

        try:
            user = query.first()
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
