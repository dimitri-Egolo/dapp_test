from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models


# Create your models here.
class UserProfileManager(BaseUserManager):
    def create_user(self, username, password=None, **kwargs):
        if not username:
            raise ValueError('Users must have a valid email username.')

        if not kwargs.get('email'):
            raise ValueError('Users must have a valid email.')

        userprofile = self.model(
            email=self.normalize_email(kwargs.get('email')), username=username
        )

        userprofile.set_password(password)
        userprofile.save()

        return userprofile

    def create_superuser(self, username, password, **kwargs):
        userprofile = self.create_user(username, password, **kwargs)

        userprofile.is_admin = True
        userprofile.is_staff = True
        userprofile.is_superuser = True
        userprofile.save()

        return userprofile


class UserProfile(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)

    first_name = models.CharField(max_length=45, blank=False, null=False)
    last_name = models.CharField(max_length=45, blank=False, null=False)
    photo = models.ImageField(upload_to='uploads/')
    tagline = models.CharField(max_length=140, blank=True)

    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name
