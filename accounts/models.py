from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Permission, Group
from django.db.models.signals import post_save
from django.db.models import Q
from django.db import models
from django.utils import timezone
from django.dispatch import receiver

from accounts.managers import UserManager



class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _("نام کاربری"),
        max_length=11,
        unique=True,
        validators=[
            RegexValidator(r'09\d{9}'),
        ],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    name = models.CharField(max_length=100, verbose_name='نام و نام خانوادگی')
    email = models.EmailField(_("آدرس ایمیل"), blank=True)
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_superuser = models.BooleanField(default=False, verbose_name='مدیر')
    is_staff = models.BooleanField(
        _("اجازه ورود"),
        default=False,
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('گروه'),
        blank=True,
        related_name="user_sets",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="user_sets",
        related_query_name="user",
    )

    objects=UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ('name',)
    EMAIL_FIELD = "email"

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربرها'
        ordering = (
            'name',
        )

