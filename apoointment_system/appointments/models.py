from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


# MODELS
class Service(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True)
    name = models.CharField(max_length=155, blank=True, null=True)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    STATES = [
        ["OK", "aproved"],
        ["PN", "pending"],
        ["CL", "canceled"]
    ]
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, blank=True, null=True)
    length = models.PositiveBigIntegerField(blank=True, null=True)
    time = models.TimeField()
    date = models.DateField()
    state = models.CharField(max_length=2, choices=STATES, default="PN",blank=True, null=True)
    notes = models.TextField(max_length=400, blank=True, null=True)

    @property
    def is_overdue(self):
        today = timezone.now()  
        return self.date <= today.date()
    
    @property
    def is_today(self):
        today = timezone.now()
        return self.date == today.date()
    
    @property
    def get_time(self):
        return self.time.strftime("%H:%M")
    
    def change_state(self):
        if self.state == 'OK': self.state = 'CL'
        elif self.state == 'PN': self.state = 'OK'
        else: self.state = 'PN'

        self.save()
        return


    def __str__(self):
        return f"{self.service} on {self.date} at {self.time.strftime('%H %M %p')}."