import json
from django.views import View
from django.shortcuts import render
from serve.models import Place, Schedule, ReservationRequest



def index(request):
    places = Place.objects.all()

    context = {
        'places': places
    }

    return render(request, 'serve/main.html', context)


class place(View):
    def get(self, request, id):
        try:
            schedule_dict = {}
            place = Place.objects.get(id=id)
            schedule_times = Schedule.objects.filter(place=place, deleted=False).order_by('time_in')
            for item in schedule_times:
                schedule_dict[item.pk] = {}
                schedule_dict[item.pk]['accept'] = 1 if ReservationRequest.objects.filter(schedule=item, status='accepted', deleted=False).exists() else 0
                schedule_dict[item.pk]['pending'] = ReservationRequest.objects.filter(schedule=item, status='pending', deleted=False).count()
                schedule_dict[item.pk]['time_in'] = item.time_in
                schedule_dict[item.pk]['time_out'] = item.time_out
                
            context = {
                'place': place,
                'schedules': schedule_dict
            }
            return render(request, 'serve/schedule.html', context)
        except:
            pass
    