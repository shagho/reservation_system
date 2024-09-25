from django.db import models
from django_jalali.db import models as jmodels



class Place(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField()
    description = models.TextField()

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'سالن'
        verbose_name_plural = 'سالن ها'


class ReservationRequest(models.Model):
    STATUS_TYPE = [
        ('accepted', 'پذیرش'),
        ('pending', 'در حال بررسی'),
        ('not accept', 'رد'),
        ('cancel', 'لغو شده')
    ]
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    status = models.CharField(max_length=16, choices=STATUS_TYPE, verbose_name='وضعیت')
    request_time = jmodels.jDateTimeField(auto_now_add=True)
    request_date = jmodels.jDateField(verbose_name = 'تاریخ درخواستی برای رزرو')
    time_in = models.TimeField(verbose_name='ساعت شروع')
    time_out = models.TimeField(verbose_name='ساعت پایان')
    place = models.ForeignKey('serve.Place', on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'درخواست رزرو'
        verbose_name_plural = 'درخواست های رزرو'
