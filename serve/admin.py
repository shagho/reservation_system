from django.contrib import admin
from django.db import models
from jalali_date_new.fields import JalaliDateTimeField, JalaliDateField
from jalali_date_new.widgets import AdminJalaliDateTimeWidget, AdminJalaliDateWidget
from .models import Place, ReservationRequest


@admin.register(ReservationRequest)
class ReservationRequestAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.DateTimeField: 
        {
            'form_class': JalaliDateTimeField,
            "widget": AdminJalaliDateTimeWidget,
        },
        models.DateField:
        {
            'form_class': JalaliDateField,
            "widget": AdminJalaliDateWidget,
        }
    }

admin.site.register(Place)
