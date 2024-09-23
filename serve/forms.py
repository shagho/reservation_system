from django import forms
from .models import ReservationRequest
from django.utils.translation import gettext_lazy as _
from jalali_date_new.fields import JalaliDateField
from jalali_date_new.widgets import AdminJalaliDateWidget, AdminJalaliTimeWidget



class ProfileForm(forms.Form):
    name = forms.CharField(max_length=128, required=True, error_messages={'required': 'این فیلد الزامی است.'})
    email = forms.EmailField(max_length=128, required=False)

    def save(self, user, data):
        user.email = data['email']
        user.name = data['name']
        user.save()


class ReservationForm(forms.ModelForm):
    class Meta:
        model = ReservationRequest
        fields = ['request_date', 'time_in', 'time_out']
        error_messages = {
            'request_date': {
              'required': _("این فیلد الزامی است."),
              'max_length': _("باید 10 رقم باشد."),
            },
            'time_in': {
              'required': _("این فیلد الزامی است."),
            },
            'time_out': {
              'required': _("این فیلد الزامی است."),
            },
        }
        widgets = {
            'time_in': AdminJalaliTimeWidget(),
            'time_out': AdminJalaliTimeWidget(),
        }

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['request_date'] = JalaliDateField(widget=AdminJalaliDateWidget)
