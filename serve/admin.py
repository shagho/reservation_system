from django.contrib import admin
from django.db import models
from django_jalali.db import models as jmodels
from django_jalali.admin.filters import JDateFieldListFilter
from admin_filter.filters import DateRangeFilter

# You need to import this for adding jalali calendar widget
from jalali_date_new.fields import JalaliDateTimeField, JalaliDateField
from jalali_date_new.widgets import AdminJalaliDateTimeWidget, AdminJalaliDateWidget, AdminJalaliTimeWidget
from .models import Place, ReservationRequest


@admin.register(ReservationRequest)
class ReservationRequestAdmin(admin.ModelAdmin):
    list_filter = (
        'status',
        ('request_date', JDateFieldListFilter),
        ('request_date', DateRangeFilter),
    )
    formfield_overrides = {
        jmodels.jDateTimeField: 
        {
            'form_class': JalaliDateTimeField,
            "widget": AdminJalaliDateTimeWidget,
        },
        jmodels.jDateField:
        {
            'form_class': JalaliDateField,
            "widget": AdminJalaliDateWidget,
        },
        models.TimeField:
        {
            "widget": AdminJalaliTimeWidget,
        }
    }

admin.site.register(Place)
