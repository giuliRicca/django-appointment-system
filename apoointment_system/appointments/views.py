from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from appointments.utils import TimeTable, WeeklyCalendar
from appointments.forms import AppointmentForm
from appointments import models
from django.core import serializers
# Create your views here.
@login_required(login_url='admin/')
def home(request):
    context = {}
    if request.method != 'POST': form = AppointmentForm(user=request.user)
    else:
        form = AppointmentForm(request.POST)
        if form.is_valid():
            new_appointment = form.save(commit=False)
            new_appointment.owner = request.user
            new_appointment.date = timezone.now().date()
            new_appointment.state = 'OK'
            new_appointment.save()
            return redirect('home')

    context['services'] = models.Service.objects.all()
    all_appointments = models.Appointment.objects.filter(owner=request.user)
    comming_up = [x for x in all_appointments if not x.is_overdue]
    today = [x for x in all_appointments if x.is_today]
    context['time_table'] = TimeTable(timezone.now().date()).render(today,request.user)
    context['today'] = today
    context['comming_up'] = comming_up
    context['form'] = form
    return render(request, 'appointments/home.html', context)

@login_required(login_url='admin/')
def calendar(request):
    context = {}
    if request.method != 'POST': form = AppointmentForm(user=request.user)
    else: 
        form = AppointmentForm(request.POST)
        print(form)
        if form.is_valid():
            new_appointment = form.save(commit=False)
            new_appointment.owner = request.user
            new_appointment.save()
            return redirect('calendar')

    week_offset = request.GET.get("week") if request.GET.get("week") else 0
    weekly_calendar = WeeklyCalendar().render(timezone.now().date() - timezone.timedelta(weeks=-int(week_offset)))
    context['week_offset'] = week_offset
    context['calendar'] = weekly_calendar
    context['form'] = form
    return render(request, 'appointments/calendar.html', context)


def update_appointment(request, id):
    appointment = get_object_or_404(models.Appointment, pk=id, owner=request.user)
    context = {}
    if request.method == 'GET':
        try:
            appointment.change_state()
        except:
            pass
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    form = AppointmentForm(instance=appointment)
    context['form'] = form

    return render(request, 'appointments/appointment.html', context)


def user_calendar(request, username):
    context = {}
    calendar_owner = get_object_or_404(get_user_model(), username=username)
    if not calendar_owner: return

    if request.method != 'POST': 
        form = AppointmentForm(user=calendar_owner)
    else:
        form = AppointmentForm(request.POST)
        if form.is_valid():
            new_appointment = form.save(commit=False)
            new_appointment.owner = calendar_owner
            new_appointment.date = timezone.now().date()
            new_appointment.state = 'PN'
            new_appointment.save()
            return redirect('home')

    today = timezone.now().date()
    appointments = models.Appointment.objects.filter(owner=calendar_owner, date=today)
    context['owner'] = calendar_owner.__str__()
    context['time_table'] = TimeTable(today).render(appointments, calendar_owner)
    context['form'] = form

    return render(request, 'appointments/user_time_table.html', context)

# 
def appoinment_data(request, id):
    appointment = get_object_or_404(models.Appointment, id=id)
    print(appointment)
    return JsonResponse({
        'service': appointment.service.id,
        'length': appointment.length,
        'notes': appointment.notes
    })


def user_settings(request):
    context = {}
    context['services'] = models.Service.objects.filter(user=request.user)
    return render(request, 'appointments/user_settings.html', context)