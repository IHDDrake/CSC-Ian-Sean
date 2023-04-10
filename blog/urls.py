from django.urls import path
from .views import Home, Detail, addPost, addBoat, upVote, downVote
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', Home.as_view(), name="homepage"),
    path('events/<int:pk>', Detail.as_view(), name="detailed_post"),
    #This url goes unused in this program
    path('add_post/', addPost.as_view(), name ='add_post'),

    path('add_boat/', addBoat.as_view(), name ='add_boat'),

    #The upvote and downvote are passed the primary key of the post so
    #they know where to return to after completing their tasks.
    path('upVote/<int:pk>', upVote, name = 'upvote'),
    path('downVote/<int:pk>', downVote, name = 'downvote')


]

#adding Static Files
urlpatterns += staticfiles_urlpatterns()
