from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('calendar/', views.calendar, name='calendar'),
    path('appointment/<str:id>/update', views.update_appointment, name='update_appointment'),
    path('appointment/<str:id>/', views.appoinment_data, name='appointment_data'),
    path('calendar/<str:username>', views.user_calendar, name='user_calendar'),
    path('settings', views.user_settings, name='settings')
]