from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
import random

class CustomUser(AbstractUser):
    phone = models.CharField(default='09196847193',
        max_length=11,
        unique=True,
        validators=[RegexValidator(r"^09\d{9}$", "شماره موبایل معتبر نیست")]
    )
    
    user_code = models.CharField(max_length=10,unique=True, blank=True, null=True,verbose_name=_('UserCode'))
    otp_code = models.CharField(max_length=6, blank=True, null=True,verbose_name=_('OptCode'))
    otp_created = models.DateTimeField(blank=True, null=True,verbose_name=_('OtpDate'))

    # این دو فیلد را غیرفعال می‌کنیم اگر نمی‌خواهی username داشته باشی:
    # username = models.CharField(max_length=150, unique=False, null=True, blank=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []  # چون phone به عنوان USERNAME است

    def generate_otp(self):
        code = str(random.randint(1000, 9999))
        self.otp_code = code
        from django.utils import timezone
        self.otp_created = timezone.now()
        self.save()
        return code




class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

    # مشخصات کاربر
    full_name = models.CharField(max_length=255, blank=True, null=True,verbose_name=_('FullName'))
    national_code = models.CharField(max_length=10, blank=True, null=True,verbose_name=_('NationalCode'))
    birth_date = models.DateField(blank=True, null=True,verbose_name=_('BirthDate'))

    # اطلاعات تماس و آدرس
    phone = models.CharField(max_length=11, blank=True, null=True,verbose_name=_('PhonNumber'))
    address = models.CharField(max_length=250, blank=True, null=True,verbose_name=_('Address'))
    postal_code = models.CharField(max_length=20, blank=True, null=True,verbose_name=_('PostalCode'))
    city = models.CharField(max_length=50, blank=True, null=True,verbose_name=_('City'))
    province = models.CharField(max_length=50, blank=True, null=True,verbose_name=_('Province'))

    # جنسیت
    gender = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name=_('Gender'),
        choices=(("male", "Male"), ("female", "Female"))
    )

    def __str__(self):
        return f"{self.user.username} Profile"
