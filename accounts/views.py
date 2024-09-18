from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django_htmx.http import trigger_client_event
from .models import User, PhoneCode
from .tasks import send_code



@method_decorator(csrf_exempt, name='dispatch')
class otpLogin(View):
    def get(self, request):
        return render(request,
                      'accounts/login.html',
                      {
                          'base_template': 'accounts/login-otp.html',
                          'sms': False
                      })
    
    def post(self, request):
        if request.htmx:
            username = request.POST['username']
            phone, created = PhoneCode.objects.get_or_create(phone_number=username)
            if phone.limitations_check():
                request.session['username'] = username
                send_code.delay(username)
                return render(request,
                              'accounts/login.html',
                              {
                                  'base_template': 'accounts/login-otp-partial.html',
                                  'sms': True
                              })
            messages.error(request, 'شماره شما دارای محدودیت می باشد.')
            response = render(request,
                              'accounts/login.html',
                              {
                                  'base_template': 'accounts/login-otp-partial.html',
                                  'sms': False
                              })
            return trigger_client_event(response, 'show_message')
        else:
            username = request.session['username']
            u_otp = request.POST['otp']
            if username and u_otp:
                phone = PhoneCode.objects.get(
                            phone_number=username
                )
                if phone.check_password(u_otp):
                    phone.tmp_code_expire = timezone.now()
                    phone.save()
                    user, created = User.objects.get_or_create(username=username)
                    login(request, user)
                    if request.GET.get('next'):
                        return redirect(request.GET.get('next'))
                    return redirect('serve:profile')
                else:
                    messages.error(request,'کد وارد شده اشتباه است.')
                    response = render(request,
                                      'accounts/login.html',
                                      {
                                        'base_template': 'accounts/login-otp.html',
                                        'sms': True
                                      })
                    return trigger_client_event(
                        response, 'show_message',
                        after="settle",
                    )
            del request.session['username']
            return redirect('login')


class Logout(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('serve:index')