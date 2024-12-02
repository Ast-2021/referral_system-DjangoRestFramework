import random
import string

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models



def get_invite_code():
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choices(characters, k=6))
    return code


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('')
        extra_fields.setdefault('invite_code', get_invite_code())
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('')
        
        return self.create_user(phone_number, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    invite_code = models.CharField(max_length=6)
    my_refer = models.CharField(max_length=6, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.phone_number)
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True