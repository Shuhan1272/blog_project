
from django.contrib.auth.base_user import BaseUserManager

#class for createsuperuser using email and password
#Note : we are creating new method name createsuperuser not overriding here. and using some methods from 
#BaseUserManager
class CustomUserManager(BaseUserManager):
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password) #password will be hashed in admin panel 
        user.save()
        return user