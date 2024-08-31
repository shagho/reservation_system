from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render,redirect
from django.views import View
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import User, PhoneCode
from .tasks import send_code



@method_decorator(csrf_exempt, name='dispatch')
class userLogin(View):
    def get(self, request):
        return render(request,'accounts/login.html')
    
    def post(self, request):
        username = request.POST['username']
        phone, created = PhoneCode.objects.get_or_create(phone_number=username)
        if phone.limitations_check():
            request.session['username'] = username
            send_code.delay(username)
            return redirect('login_otp')
        messages.error(request, 'شماره شما دارای محدودیت می باشد.')
        return render(request,'accounts/login.html')


@method_decorator(csrf_exempt, name='dispatch')
class otpLogin(View):
    def get(self, request):
        return render(request,'accounts/login-otp.html')
    
    def post(self, request):
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
                return redirect('dashboard')
            else:
                messages.error(request,'کد وارد شده اشتباه است.')
                return render(request,'accounts/login-otp.html')
        else:
            redirect('login')