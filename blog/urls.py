from django.urls import path
from .views import Home, Detail, addBoat, deleteBoat, unregister
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', Home.as_view(), name="homepage"),
    path('events/<int:pk>', Detail.as_view(), name="detailed_post"),
    path('add_boat/', addBoat.as_view(), name ='add_boat'),
    path('deleteBoat/<int:pk>', deleteBoat, name='deleteBoat'),
    path('unregister/<int:pk>/<int:epk>', unregister, name='unregister')


]

#adding Static Files
urlpatterns += staticfiles_urlpatterns()
