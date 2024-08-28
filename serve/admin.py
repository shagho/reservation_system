from django.contrib import admin
from django.db import models
from jalali_date_new.fields import JalaliDateTimeField
from jalali_date_new.widgets import AdminJalaliDateTimeWidget
from .models import Place, Schedule, ReservationRequest


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.DateTimeField: 
        {
            'form_class': JalaliDateTimeField,
            "widget": AdminJalaliDateTimeWidget,
        },
    }

admin.site.register(Place)
admin.site.register(ReservationRequest)
