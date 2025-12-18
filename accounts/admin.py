from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    # ✅ نمایش صحیح تیک
    list_display = (
        'phone',
        'user_code',
        'is_affiliate',
        'is_staff',
        'is_active',
    )

    list_filter = (
        'is_affiliate',
        'is_staff',
        'is_active',
    )

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('اطلاعات شخصی', {'fields': ('first_name', 'last_name')}),
        ('Affiliate', {'fields': ('is_affiliate',)}),
        ('دسترسی‌ها', {
            'fields': (
                'is_staff',
                'is_active',
                'is_superuser',
                'groups',
                'user_permissions'
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'phone',
                'first_name',
                'last_name',
                'password1',
                'password2',
                'is_affiliate',
                'is_staff',
                'is_active',
            ),
        }),
    )

    search_fields = ('phone',)
    ordering = ('phone',)
