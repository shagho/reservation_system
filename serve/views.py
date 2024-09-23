import json
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from serve.forms import ProfileForm, ReservationForm
from serve.models import Place, ReservationRequest



def index(request):
    places = Place.objects.all()

    context = {
        'places': places
    }

    return render(request, 'serve/main.html', context)


class place(View):
    def get(self, request, id):
        place = Place.objects.get(id=id)
            
        context = {
            'place': place,
        }
        return render(request, 'serve/schedule.html', context)


class AcceptReservation(LoginRequiredMixin, View):
    login_url = "/login/"
    def post(self, request, id):
        reservation = ReservationForm(request.POST)

        if reservation.is_valid():
            instance = reservation.save(commit=False)
            query = ReservationRequest.objects.filter(place_id=id, request_date=instance.request_date)

            if query.filter(user=request.user).exists():
                messages.error(request=request, message="شما قبلا برای این مکان در این تاریخ درخواست ثبت کرده اید.")
                return redirect('serve:place_view', id=id)

            if query.filter(status='accepted').exists():
                messages.error(request=request, message="مکان در این زمان قابل رزو نمی باشد.")
                return redirect('serve:place_view', id=id)

            if query.filter(status='pending').exists() or not query.exists():
                instance.user = request.user
                instance.status = 'pending'
                instance.place_id = id
                instance.save()
                messages.warning(request=request, message="رزرو شما در صف انتظار می باشد. پس از تایید می توانید پرداخت را انجام دهید.")
                return redirect('serve:my_reservation')
        
        return redirect('serve:place_view', id=id)
            

class MyReservation(LoginRequiredMixin, View):
    login_url = "/login/"
    def get(self, request):
        page_number = request.GET.get("page", 1)
        reservations = ReservationRequest.objects.filter(user=request.user).order_by('-request_time')
        paginator = Paginator(reservations, 25)
        try:
            reservations = paginator.page(page_number)
        except PageNotAnInteger:
            reservations = paginator.page(1)
        except EmptyPage:
            reservations = paginator.page(paginator.num_pages)
            
        return render(request, "serve/my_reservation.html", {"reservations": reservations})
    
    def delete(self, request, id):
        reservation_request = get_object_or_404(ReservationRequest, id=id)
        response_message = {'message': 'لغو شده', 'show-toast': None}

        if request.user == reservation_request.user:
            reservation_request.status = 'cancel'
            reservation_request.save()

            response_message['show-toast'] = json.dumps({
                "show-toast": {
                    "level": "success",
                    "message": "رزرو با موفقیت لغو شد."
                }
            })

        response = HttpResponse('لغو شده')
        if response_message['show-toast']:
            response['HX-Trigger'] = response_message['show-toast']

        return response


@method_decorator(csrf_exempt, name='dispatch')
class Profile(View):
    login_url = "/login/"
    def get(self, request):
        context = {
            'email': request.user.email,
            'name': request.user.name,
        }

        form = ProfileForm(context)
        return render(request, 'serve/profile.html', context={"form": form})

    def post(self, request):
        form = ProfileForm(request.POST)

        if form.is_valid():
            form.save(request.user, form.cleaned_data)
            messages.success(request, 'اطلاعات شما با موفقیت ذخیره شد.')
        return render(request, 'serve/profile.html', context={"form": form})
    