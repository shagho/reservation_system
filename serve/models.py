from django.db import models
from django_jalali.db import models as jmodels



class Place(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField()
    description = models.TextField()

    def __str__(self) -> str:
        return self.name


class Schedule(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    time_in = jmodels.jDateTimeField()
    time_out = jmodels.jDateTimeField()
    deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.place.name + ' ' + str(self.time_in.date()) + ':' + str(self.time_in.time()) + ',' + str(self.time_out.date()) + ':' + str(self.time_out.time())


class ReservationRequest(models.Model):
    STATUS_TYPE = [
        ('accepted', 'پذیرش'),
        ('pending', 'در حال بررسی'),
        ('not accept', 'رد شده'),
        ('cancel', 'لغو شده')
    ]
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    schedule = models.ForeignKey('serve.Schedule', on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=16, choices=STATUS_TYPE)
    request_time = jmodels.jDateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
