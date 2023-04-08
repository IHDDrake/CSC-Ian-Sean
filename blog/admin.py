from django.contrib import admin
from .models import Event, Comment

# Registering models
admin.site.register(Event)
admin.site.register(Comment)
