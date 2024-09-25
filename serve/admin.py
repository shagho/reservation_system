import jdatetime
from django.contrib import admin
from django.db import models
from django_jalali.db import models as jmodels
from django_jalali.admin.filters import JDateFieldListFilter
from admin_filter.filters import DateRangeFilter
from import_export import resources, fields
from import_export.admin import ExportMixin
from import_export.widgets import ForeignKeyWidget, DateWidget
from jalali_date_new.fields import JalaliDateTimeField, JalaliDateField
from jalali_date_new.widgets import AdminJalaliDateTimeWidget, AdminJalaliDateWidget, AdminJalaliTimeWidget
from accounts.models import User
from .models import Place, ReservationRequest



class JalaliDateWidget(DateWidget):
    def render(self, value, obj=None):
        if value:
            return str(value)
        return ''


class ReservationRequestResource(resources.ModelResource):
    user = fields.Field(
        column_name='user',
        attribute='user',
        widget=ForeignKeyWidget(User, field='username'))
    place = fields.Field(
        column_name='place',
        attribute='place',
        widget=ForeignKeyWidget(User, field='name'))
    request_date = fields.Field(
        column_name='request_date',
        attribute='request_date',
        widget=JalaliDateWidget(format='%Y-%m-%d'))
    status = fields.Field(
        column_name='status',
        attribute='get_status_display'
    )

    def get_fields(self, **kwargs):
        """
        Override to display the verbose names of the fields in the 'Select Fields to Export' page.
        """
        fields = super().get_fields(**kwargs)
        for field in fields:
            # Get verbose name if it exists, otherwise use the field name
            field_name = field.column_name
            try:
                verbose_name = self.Meta.model._meta.get_field(field_name).verbose_name
            except: verbose_name = field_name
            # Replace the field name with its verbose name
            field.column_name = verbose_name.title() if verbose_name else field_name
        return fields

    def get_export_headers(self, fields=None):
        headers = []
        for field in self.get_export_fields():
            headers.append(field.column_name)
        
        return headers
    
    class Meta:
        model = ReservationRequest
        fields = ('user', 'place', 'request_date', 'time_in', 'time_out', 'status')


@admin.register(ReservationRequest)
class ReservationRequestAdmin(ExportMixin, admin.ModelAdmin):
    resource_classes = [ReservationRequestResource]
    list_filter = (
        'status',
        ('request_date', JDateFieldListFilter),
        ('request_date', DateRangeFilter),
    )
    list_display = ('user', 'place', 'request_date', 'time_in', 'time_out', 'status')

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
