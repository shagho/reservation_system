import jdatetime

from django.contrib.admin.filters import FieldListFilter
from jalali_date_new.widgets import AdminJalaliDateTimeWidget
from collections import OrderedDict

from django import forms
from django.template.defaultfilters import slugify
from django.templatetags.static import StaticNode
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from django.conf import settings



class DateRangeFilter(FieldListFilter):
    _request_key = "DJANGO_RANGEFILTER_ADMIN_JS_LIST"
    template = 'admin_filter/date_filter.html'
    
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.field_generic = "%s__" % field_path
        self.lookup_kwarg_since = "%s__gte" % field_path
        self.lookup_kwarg_until = "%s__lt" % field_path
        self.title = self._get_default_title(request, model_admin, field_path)
        self.default_gte, self.default_lte = self._get_default_values(
            request, model_admin, field_path
        )
        self.links = ()
        if field.null:
            self.lookup_kwarg_isnull = "%s__isnull" % field_path
            self.links += (
                (_("No date"), {self.field_generic + "isnull": "True"}),
                (_("Has date"), {self.field_generic + "isnull": "False"}),
            )
        super().__init__(field, request, params, model, model_admin, field_path)
        self.request = request
        self.form = self.get_form(request)

    def expected_parameters(self):
        params = [self.lookup_kwarg_since, self.lookup_kwarg_until]
        if self.field.null:
            params.append(self.lookup_kwarg_isnull)
        return params
    
    def _get_default_values(self, request, model_admin, field_path):
        if hasattr(self, "__from_builder"):
            return self.default_start, self.default_end

        default_method_name = "get_rangefilter_{0}_default".format(field_path)
        default_method = getattr(model_admin, default_method_name, None)

        if not callable(default_method):
            return None, None

        return default_method(request)

    def _get_default_title(self, request, model_admin, field_path):
        if hasattr(self, "__from_builder"):
            return self.default_title or self.title

        title_method_name = "get_rangefilter_{0}_title".format(field_path)
        title_method = getattr(model_admin, title_method_name, None)

        if not callable(title_method):
            return self.title

        return title_method(request, field_path)
    
    @staticmethod
    def make_dt_aware(value, tzname):
        if settings.USE_TZ:
            value = value.replace(tzinfo=tzname)
        return value
    
    def get_timezone(self, _request):
        return timezone.get_current_timezone()
    
    def _make_query_filter(self, request, validated_data):
        query_params = {}
        date_value_gte = validated_data.get(self.lookup_kwarg_since, None)
        date_value_lte = validated_data.get(self.lookup_kwarg_until, None)

        if date_value_gte:
            query_params[self.lookup_kwarg_since] = self.make_dt_aware(
                jdatetime.datetime(date_value_gte.year, date_value_gte.month, date_value_gte.day, 0, 0, 0, 0).togregorian(),
                self.get_timezone(request),
            )
        if date_value_lte:
            query_params[self.lookup_kwarg_until] = self.make_dt_aware(
                jdatetime.datetime(date_value_lte.year, date_value_lte.month, date_value_lte.day, 23, 59, 59, 999).togregorian(),
                self.get_timezone(request),
            )

        return query_params

    def queryset(self, request, queryset):
        if self.form.is_valid():
            validated_data = dict(self.form.cleaned_data.items())
            if validated_data:
                return queryset.filter(**self._make_query_filter(request, validated_data))
        return queryset

    def choices(self, changelist):
        yield {
            # slugify converts any non-unicode characters to empty characters
            # but system_name is required, if title converts to empty string use id
            # https://github.com/silentsokolov/django-admin-rangefilter/issues/18
            "system_name": force_str(
                slugify(self.title) if slugify(self.title) else id(self.title)
            ),
            "query_string": changelist.get_query_string({}, remove=self.expected_parameters()),
        }

    def _get_form_fields(self):
        return OrderedDict(
            (
                (
                    self.lookup_kwarg_since,
                    forms.DateField(
                        label="",
                        widget=AdminJalaliDateTimeWidget(attrs={"placeholder": _("From date"), 'data-jdp':''}),
                        localize=True,
                        required=False,
                        initial=self.default_gte,
                    ),
                ),
                (
                    self.lookup_kwarg_until,
                    forms.DateField(
                        label="",
                        widget=AdminJalaliDateTimeWidget(attrs={"placeholder": _("To date"), 'data-jdp':''}),
                        localize=True,
                        required=False,
                        initial=None,
                    ),
                ),
            )
        )
    
    def _get_form_class(self):
        fields = self._get_form_fields()

        form_class = type(str("DateRangeForm"), (forms.BaseForm,), {"base_fields": fields})

        # lines below ensure that the js static files are loaded just once
        # even if there is more than one DateRangeFilter in use
        js_list = getattr(self.request, self._request_key, None)
        if not js_list:
            js_list = (
                # StaticNode.handle_simple("admin_filter/js/datepicker.js"),
                # StaticNode.handle_simple("admin_filter/js/jalalidatepicker.min.js"),
            )
            setattr(self.request, self._request_key, js_list)

        form_class.js = js_list

        return form_class

    def get_form(self, _request):
        form_class = self._get_form_class()
        return form_class(self.used_parameters or None)
