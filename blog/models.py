from django.db import models
from django.urls import reverse
from django.contrib.auth.models import  User
from django.utils import timezone




class Event(models.Model):
    heroHeader = models.ImageField(upload_to ='uploads/', default=None, blank=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    body = models.TextField()
    event_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    viewCount = models.IntegerField(default=0)
    pubStatus = models.BooleanField(default=False)


    #Basic Object to string method
    def __str__(self):
        return self.title + ' by ' + str(self.author)

    #Returns Url for the Details page of a sepcific post
    def get_absolute_url(self):
        return reverse('detailed_post', args=[str(self.id)])
    
    @property
    def future(self):
        return self.event_time > timezone.now()
    
    
    

class Boat(models.Model):
    owner = models.ForeignKey(User,verbose_name="User",related_name="owner", on_delete=models.CASCADE)  # noqa: E501
    classification = models.CharField(max_length=3)
    number = models.CharField(max_length=4)
    def __str__(self):
        return str(self.classification) + str(self.number) 
    
    def get_success_url(self):
        return reverse('homepage', args=[str(self.id)])
    
    def get_absolute_url(self): 
        return reverse('homepage', args=[str(self.id)])
    
class Registration(models.Model):
    event = models.ForeignKey(Event, related_name="regs", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    ranking = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user) 

