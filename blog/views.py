from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, CreateView, FormView
from django.http import HttpResponseRedirect
from .models import Event, Comment, Boat, Registration
from .forms import BoatForm, RegistrationForm
from django.contrib.auth.models import User



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
        context['form'] = RegistrationForm(user=self.request.user)
        try:
            context['regist'] = Registration.objects.filter(user=self.request.user, event=self.object).exists()  
            context['registR']= Registration.objects.filter(user=self.request.user, event=self.object)
        finally:
            return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
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
        return HttpResponseRedirect(reverse('add_boat'))


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

def deleteBoat(request, pk):
    boat = get_object_or_404(Boat, pk=pk, owner=request.user)
    boat.delete()
    return HttpResponseRedirect(reverse('add_boat'))

def unregister(request, pk, epk):
    boat = get_object_or_404(Registration, pk=pk, user=request.user)
    boat.delete()
    return HttpResponseRedirect(reverse('detailed_post', args=[str(epk)]))
