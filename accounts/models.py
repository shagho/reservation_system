from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Permission, Group
from django.db.models.signals import post_save
from django.db.models import Q
from django.db import models
from django.utils import timezone

from notifications import KavenegarSMS
from accounts import utils
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
    company_name = models.CharField(max_length=128, null=True, blank=True, verbose_name='نام شرکت')
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

    def __str__(self):
        return self.company_name or self.name or self.username


class SMSBlackList(models.Model):
    phone_number = models.CharField(
        max_length=11,
        null=True,
        blank=True,
        verbose_name='phone number',
        validators=[
            RegexValidator(r'09\d{9}'),
        ]
    )
    ip = models.GenericIPAddressField(null=True, blank=True)
    insert_time = models.DateTimeField(auto_now_add=True)
    expire_time = models.DateTimeField(null=True, blank=True)


class PhoneCode(models.Model):
    phone_number = models.CharField(
        max_length=11,
        null=True,
        blank=True,
        verbose_name='phone number',
        unique=True,
        validators=[
            RegexValidator(r'09\d{9}'),
        ],
    )
    tmp_code = models.CharField(max_length=6, default=utils.password_generator)
    tmp_code_expire = models.DateTimeField(default=timezone.now)
    tmp_code_sent_time = models.DateTimeField(default=utils.five_minute_ago)
    tmp_code_sent_counter_in_last_24_hour = models.IntegerField(default=0)
    def check_password(self, password):
        """
            check if password is valid for time been
            returnin Boolean True for Valid
        """
        if self.tmp_code_expire > timezone.now() and \
                self.tmp_code == password:
            return True
        return False

    def __can_request_sms(self):
        """
            check if user is allowed to send a request for another sms verification
            returning Boolean True for allowed to send another sms verification
        """
        block = SMSBlackList.objects.filter(
            Q(phone_number = self.phone_number),
            Q(expire_time__isnull=True) |
            Q(expire_time__gt=timezone.now())
        )
        if block.exists():
            return False
        if self.tmp_code_sent_time > timezone.now() - timezone.timedelta(minutes=1):
            return None
        self.save()
        if self.tmp_code_sent_counter_in_last_24_hour < 15:
            return True
        return False

    def limitations_check(self):
        condition = self.__can_request_sms()
        if condition is None:
            return True
        elif condition:
            if self.tmp_code_sent_time.date() == timezone.now().date():
                self.tmp_code_sent_counter_in_last_24_hour += 1
            else:
                self.tmp_code_sent_counter_in_last_24_hour = 0
            self.save()
            return True
        return False

    def send_tmp_code(self):
        """
            sending kavenegar sms 
            returning Boolean True for sended
        """
        tmp = self.__can_request_sms()
        if tmp is None:
            return True
        elif tmp:
            self.tmp_code = utils.password_generator()
            self.tmp_code_expire = utils.five_minute_later()
            sms = KavenegarSMS()
            sms.register(
                receptor=self.phone_number,
                code=self.tmp_code,
            )
            sms.send()
            self.tmp_code_sent_time = timezone.now()
            self.save()
            return True
        return False

    def send_code(self):
        self.tmp_code = utils.password_generator()
        self.tmp_code_expire = utils.five_minute_later()
        sms = KavenegarSMS()
        sms.register(
            receptor=self.phone_number,
            code=self.tmp_code,
        )
        print(sms.send())
        self.tmp_code_sent_time = timezone.now()
        self.save()
        return True