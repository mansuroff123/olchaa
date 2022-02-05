from django.core.exceptions import ValidationError
from users.models import UserModel


class PhoneValidatorTest:
    requires_context = False

    def __call__(self, value):
        if not UserModel.objects.filter(phone=value).exists():
            raise ValidationError("Bu telefon raqami mavjud emas!")