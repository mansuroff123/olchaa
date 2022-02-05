from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.safestring import mark_safe

from config.validators import PhoneValidator
from datetime import datetime
import os
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.conf import settings
from django.core.exceptions import ValidationError

class UserManager(BaseUserManager):
    def __create_user(self, phone, password, **kwargs):
        phone = PhoneValidator.clean(phone)
        # validator = PhoneValidator()
        # validator(phone)

        if not PhoneValidator.validate(phone):
            raise ValidationError("Tel no'mer emas")

        user = UserModel(**kwargs)
        user.phone = phone
        user.set_password(password)

        user.save()

    def create_user(self, *args, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)

        if kwargs.get('is_staff') or kwargs.get('is_superuser'):
            raise Exception("User is_staff=False va is_superuser=False bo'lishi shart")

        return self.__create_user(*args, **kwargs)

    def create_superuser(self, *args, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        if not kwargs.get('is_staff') or not kwargs.get('is_superuser'):
            raise Exception("User is_staff=True va is_superuser=True bo'lishi shart")

        # print(args, kwargs)

        return self.__create_user(*args, **kwargs)

    def get_by_natural_key(self, username):
        return UserModel.objects.get(username=username)


def convert_fn(ins, file):
    ext = file.split('.')[-1]
    filename = '{:%Y-%m-%d-%H-%M-%S}.{}'.format(datetime.now(), ext)
    return os.path.join('user_pick',filename)


# def convert_fn(ins, file):
#     ext = file.split('.')[-1]
#     filename = '{:%Y-%m-%d-%H-%M-%S}.{}'.format(datetime.now(), ext)
#     return os.path.join('post_pics', filename)


class UserModel(AbstractUser):
    objects = UserManager()
    password = models.CharField(max_length=100, help_text="Пожалуйста, укажите свой пароль")
    phone = models.CharField(max_length=15, unique=True,
                             validators=[PhoneValidator()],  help_text="Пожалуйста, предоставьте свой телефон")
    avatar = models.ImageField(upload_to=convert_fn, null=True, blank=True)

    USERNAME_FIELD = 'phone'
    username_validator = PhoneValidator()

    @property
    def full_name(self):
        return "{} {}".format(self.last_name, self.first_name)

    def admin_image(self):
        return mark_safe('<img src="{}" width="60" />'.format(self.image_url))

    def save(self, *args, **kwargs):
        if not self.avatar.closed:
            image = Image.open(self.avatar)
            image.thumbnail((1000, 1000), Image.ANTIALIAS)

            tmp = BytesIO()
            image.save(tmp, "PNG")

            self.avatar = File(tmp, 't.png')
        super().save(*args, **kwargs)

    @property
    def image_url(self):
        if self.avatar:
            return os.path.join(settings.MEDIA_URL, str(self.avatar))

        return os.path.join(settings.STATIC_URL, "main/img/nophoto.png")

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

