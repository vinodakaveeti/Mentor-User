from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from rest_framework_simplejwt.tokens import RefreshToken

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the username
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email_):
        return self.get(email=email_)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_mentor = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access_token': str(refresh.access_token)
        }


class Conversation(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sender1', on_delete=models.CASCADE, null=True)
    receipient = models.ForeignKey(CustomUser, related_name='receipient1', on_delete=models.CASCADE, null=True)
    conversation = models.TextField(max_length=500)
    sent_at = models.DateTimeField(default=now, editable=True, null=True, blank=True)
    reply = models.TextField(max_length=500, null=True, blank=True)
    reply_at = models.DateTimeField(editable=True, null=True, blank=True)
    document = models.FileField(upload_to='files/', blank=True, null=True)

    class Meta:
        ordering = ['-sent_at']

    def save(self, *args, **kwargs):
        if self.reply:
            self.reply_at = now()
        super(Conversation, self).save(*args, **kwargs)

    @property
    def get_sender_email(self):
        return self.sender.email
