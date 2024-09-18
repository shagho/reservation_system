import json
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from serve.forms import ProfileForm
from serve.models import Place, Schedule, ReservationRequest



def index(request):
    places = Place.objects.all()

    context = {
        'places': places
    }

    return render(request, 'serve/main.html', context)


class place(View):
    def get(self, request, id):
        schedule_dict = {}
        place = Place.objects.get(id=id)
        schedule_times = Schedule.objects.filter(place=place, deleted=False).order_by('time_in')
        for item in schedule_times:
            schedule_dict['date'] = schedule_dict.get('date', {})
            schedule_dict['date'][str(item.time_in.date())] = schedule_dict['date'].get(str(item.time_in.date()), {})
            schedule_dict['date'][str(item.time_in.date())][item.pk] = {}
            schedule_dict['date'][str(item.time_in.date())][item.pk]['url'] = reverse('serve:accept_reservation', args=[item.pk])
            schedule_dict['date'][str(item.time_in.date())][item.pk]['accept'] = 1 if ReservationRequest.objects.filter(schedule=item, status='accepted', deleted=False).exists() else 0
            schedule_dict['date'][str(item.time_in.date())][item.pk]['pending'] = ReservationRequest.objects.filter(schedule=item, status='pending', deleted=False).count()
            schedule_dict['date'][str(item.time_in.date())][item.pk]['time_in'] = item.time_in.time().strftime("%H:%M")
            schedule_dict['date'][str(item.time_in.date())][item.pk]['time_out'] = item.time_out.time().strftime("%H:%M")
            
        context = {
            'place': place,
            'schedules': schedule_dict
        }
        return render(request, 'serve/schedule.html', context)


class AcceptReservation(LoginRequiredMixin, View):
    login_url = "/login/"
    def get(self, request, id):
        query = ReservationRequest.objects.filter(schedule_id=id)
        
        if query.filter(user=request.user):
            messages.error(request=request, message="شما قبلا برای این مکان در این زمان درخواست ثبت کرده اید.")
            return redirect('serve:place_view', id=query[0].schedule.place.pk)
        
        if query.filter(status='accepted').exists():
            messages.error(request=request, message="مکان در این زمان قابل رزو نمی باشد.")
            return redirect('serve:place_view', id=query[0].schedule.place.pk)

        if query.filter(status='pending').exists() or not query.exists():
            ReservationRequest.objects.create(schedule_id=id, user=request.user, status='pending')
            messages.warning(request=request, message="رزرو شما در صف انتظار می باشد. پس از تایید می توانید پرداخت را انجام دهید.")
            return redirect('serve:my_reservation')
        
        return redirect('serve:place_view', id=query[0].schedule.place.pk)
            

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