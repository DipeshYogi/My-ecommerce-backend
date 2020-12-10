from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                       PermissionsMixin                                   
from django.utils import timezone


class UserManager(BaseUserManager):

    def _create_user(self, email, name, phone, password, date_of_birth, \
                     user_type, is_staff, is_superuser):

        if not email:
            raise ValueError("Users must have email address")
        if not name:
            raise ValueError("User must have a name")
        if not phone:
            raise ValueError("User must have a phone number")

        user = self.model(
            email = self.normalize_email(email),
            name = name,
            phone = phone,
            date_of_birth = date_of_birth,
            user_type = user_type,
            is_staff = is_staff,
            is_superuser = is_superuser
        )

        user.set_password(password)

        user.save(using=self._db)
        return user
    
    def create_user(self, email, name, phone, password, date_of_birth, user_type):
        """Save and Create new user"""
        return self._create_user(email, name, phone, password, date_of_birth, \
                                 user_type, False, False)

    def create_superuser(self, email, name, phone, password, date_of_birth=None, \
                         user_type="ADMIN"):
        """Save and Create new superuser"""
        user = self._create_user(email, name, phone, password, date_of_birth,\
                                 user_type, True, True )
        return user



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=12)
    date_of_birth = models.DateField(blank=True, null=True)

    user_types_choices = (("CUSTOMER", "CUSTOMER"),
                          ("SHOPKEEPER", "SHOPKEEPER"),
                          ("ADMIN", "ADMIN"))

    user_type = models.CharField(max_length=20, choices = user_types_choices)
    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default = timezone.now)
    last_login = models.DateTimeField(null=True) 

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone', 'user_type']

    def get_full_name(self):
        return self.name
    
    def get_phone_no(self):
        return self.phone 
    
    def get_email_addr(self):
        return self.email
