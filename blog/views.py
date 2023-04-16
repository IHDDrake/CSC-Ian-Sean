from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, CreateView, FormView, TemplateView
from django.http import HttpResponseRedirect
from .models import Event, Comment, Boat, Registration
from .forms import CommentForm, BoatForm, RegistrationForm
from django.contrib.auth.models import User
from django import forms


#This is the class-based view for a very simple homepage.
#It is ordered by negative creation time. This results in the object_list being
#ordered with the most recent posts at the top
class Home(ListView):
    model = Event
    template_name = 'homepage.html'
    ordering = ['-created_at']


#This is the class-based view for the Detailed Post page.
#Included are a function that update the viewCount every time the page is visited,
#a function to correctly point the url to the right post,
#and a function to ensure that forms are submitted correctly



   
   

class Detail(DetailView, FormView):
    model = Event
    form_class = RegistrationForm
    
    template_name = 'postDetails.html'
    def get_object(self):
        obj = super().get_object()
        obj.viewCount += 1
        obj.save()
        return obj
    
    def get_success_url(self):
        return reverse_lazy('detailed_post', kwargs={'pk': self.kwargs['pk']})
    
    def form_valid(self, form):
        registration = form.save(commit=False)
        registration.event = self.get_object()
        registration.user = self.request.user
        registration.boat = form.cleaned_data['boat']
        registration.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['regist'] = Registration.objects.filter(user=self.request.user, event=self.object).exists()
        finally:
            return context
    """
    def get(self, request, pk):
        user = request.user
        try:
            my_obj = Registration.objects.get(user=user, event=pk)
        except Registration.DoesNotExist:
            my_obj = ""

        context = {
            'my_obj': my_obj,
            'event': pk,
        }

        return render(request, self.template_name, context)
    """
    



#This class-based view goes unused in the final product. It remains for the purpose of remimplementation upon request


class addPost(CreateView):
    model = Event
    template_name = 'addPost.html'
    fields = '__all__'

class addBoat(CreateView, ListView):
    model = Boat
    form_class = BoatForm
    template_name = 'addBoat.html'
    
    
    def form_valid(self, form):
        candidate = form.save(commit=False)
        candidate.owner = User.objects.get(pk=self.request.user.pk)  # use your own profile here
        candidate.save()
        return HttpResponseRedirect(reverse('homepage'))


# These are the two function based views. They have no associated template and allow for the functionality
#of the comment liking and disliking buttons. Upon modify the specific comments value in the database.
#After their task is completed they redirect back to the detailed post page the comment is on.
#An improvement that can be made for these functions is the inclusion of handling a failed search.
#i.e. if get_object_or_404 doesn't retrieve whats it is asked to.
def upVote(request, pk):
    comment = get_object_or_404(Comment, id=request.EVENT.get('upvoteID'))
    comment.upVote += 1
    comment.save()
    return HttpResponseRedirect(reverse('detailed_post', args=[str(pk)]))
def downVote(request, pk):
    comment = get_object_or_404(Comment, id=request.EVENT.get('downvoteID'))
    comment.downVote -= 1
    comment.save()
    return HttpResponseRedirect(reverse('detailed_post', args=[str(pk)]))
