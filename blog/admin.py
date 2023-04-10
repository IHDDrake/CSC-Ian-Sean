from django.contrib import admin
from .models import Event, Comment, Boat

# Registering models
admin.site.register(Event)
#admin.site.register(Comment)
admin.site.register(Boat)