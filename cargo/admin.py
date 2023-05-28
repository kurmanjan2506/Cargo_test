from django.contrib import admin

from .models import Cargo, Location, Car

admin.site.register(Cargo)
admin.site.register(Car)
admin.site.register(Location)