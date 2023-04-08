from django.urls import path
from .views import UserRegisterView
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
]

#adding Static Files
#urlpatterns += staticfiles_urlpatterns()
