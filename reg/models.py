from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager

# Create your models here.

class UserManger(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("email address is mandatory")
        user = self.model(
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        print("Creating Super user using the provided method")
        user.save(using = self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(regex = r'^(\+\d{1,3}[- ]?)?\d{10}$', message="Indian mobile number. Include +91-")

    first_name = models.CharField(max_length=100, blank=True, default='user')
    last_name = models.CharField(max_length=50, blank=True,)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True,)
    mobile_number = models.CharField(validators=[phone_regex], max_length=15)
    gender = models.CharField(max_length=10)
    dob = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='uploads/', default='images/blank-profile-pic.png')
    date_joined = models.DateField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManger()

    USERNAME_FIELD = 'email'

    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = []

    def email_user(self,subject, message, from_email=None, **kwargs):
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.email