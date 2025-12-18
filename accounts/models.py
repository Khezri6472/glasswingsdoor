from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
import random
from django.utils import timezone

class CustomUser(AbstractUser):
    phone = models.CharField(
        max_length=11,
        unique=True,
        validators=[RegexValidator(r"^09\d{9}$", "شماره موبایل معتبر نیست")],verbose_name=_('Mobile Number')
    )

    otp_code = models.CharField(max_length=4, blank=True, null=True,verbose_name=_('Otp Code'))
    otp_created = models.DateTimeField(blank=True, null=True,verbose_name=_('Otp Create Date'))
    user_code=models.CharField(unique=True,max_length=10, blank=True, null=True)
    is_affiliate = models.BooleanField(default=False,verbose_name=_('Affiliate User'))
    
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["username"]  # مهم

    def generate_otp(self):
        code = str(random.randint(1000, 9999))
        self.otp_code = code
        self.otp_created = timezone.now()
        self.save(update_fields=["otp_code", "otp_created"])
        return code



class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

    # مشخصات کاربر
    full_name = models.CharField(max_length=255, blank=True, null=True,verbose_name=_('FullName'))
    national_code = models.CharField(max_length=10, blank=True, null=True,verbose_name=_('NationalCode'))
    birth_date = models.DateField(blank=True, null=True,verbose_name=_('BirthDate'))

    # اطلاعات تماس و آدرس
    phone = models.CharField(max_length=11, blank=True, null=True,verbose_name=_('Phon Number'))
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
