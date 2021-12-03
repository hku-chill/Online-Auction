from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test

class helper():

    def check_user_exist(self, email):
        if User.objects.filter(email=email).exists():
            return True
        else:
            return False





def check_user(user):
        return not user.is_authenticated


user_logout_required = user_passes_test(check_user, '/', None)


def auth_user_should_not_access(viewfunc):
    return user_logout_required(viewfunc)