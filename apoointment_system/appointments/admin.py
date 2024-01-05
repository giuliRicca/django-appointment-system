from django.contrib import admin

# Import models
from appointments import models
# Register your models here.

admin.site.register([models.Service, models.Appointment])