from django.contrib import admin
from .models import Event,  Boat,Registration

# Registering models
admin.site.register(Event)
#admin.site.register(Comment)
admin.site.register(Boat)
admin.site.register(Registration)