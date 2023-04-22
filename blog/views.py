from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, CreateView, FormView
from django.http import HttpResponseRedirect
from .models import Event, Boat, Registration
from .forms import BoatForm, RegistrationForm
from django.contrib.auth.models import User



class Home(ListView):
    model = Event
    template_name = 'homepage.html'
    ordering = ['-created_at']

 

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
            context['regist'] = Registration.objects.filter(user=self.request.user, event=self.object).exists()    # noqa: E501
            context['registR']= Registration.objects.filter(user=self.request.user, event=self.object)    # noqa: E501
            context['registResult']= Registration.objects.filter(event=self.object).order_by('ranking') # noqa: E501
        finally:
            return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs



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
        user= User.objects.get(pk=self.request.user.pk)  # use your own profile here
        candidate.owner = user
        num = form.cleaned_data['number']
        cla = form.cleaned_data['classification']
        if Boat.objects.filter(owner=user, number=num, classification=cla).exists():
            pass
        else:
            candidate.save()
        return HttpResponseRedirect(reverse('add_boat'))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['boatU'] = Boat.objects.filter(owner=self.request.user).exists()    # noqa: E501
        finally:
            return context

def deleteBoat(request, pk):
    boat = get_object_or_404(Boat, pk=pk, owner=request.user)
    boat.delete()
    return HttpResponseRedirect(reverse('add_boat'))

def unregister(request, pk, epk):
    boat = get_object_or_404(Registration, pk=pk, user=request.user)
    boat.delete()
    return HttpResponseRedirect(reverse('detailed_post', args=[str(epk)]))
