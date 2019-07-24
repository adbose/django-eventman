from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from events.forms import EventForm, ParticipationForm
from events.models import Event
from django.views.generic import ListView, DetailView


@login_required
def home(request):
    return render(request, 'home.html')


def logout_view(request):
    logout(request)
    return redirect('login')


class Signup(View):
    def get(self, request):
        form = UserCreationForm(request.GET)
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})


class EventsListView(ListView):
    model = Event
    context_object_name = 'events_list'
    template_name = 'events.html'


class EventDetailView(DetailView):
    model = Event
    context_object_name = 'event_detail'
    template_name = 'event_detail.html'


    #
    #
    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        # context['event'] = self.get_object()
        # print(context['event'])
        event = self.get_object()
        print(event)
        print(event.id)
        request = self.request
        print(request.user)
        request.session['event_id'] = event.id
        return context


class ParticipationView(View):

    def get(self, request):
        form = ParticipationForm(request.GET)
        user = request.user
        event_id = request.session['event_id']
        event = Event.objects.get(pk=event_id)

        return render(request, 'participate.html', {'form': form, 'user': user, 'event': event})

    def post(self, request):
        print('Inside Participate view...')
        user = request.user
        print(user)
        event_id = request.session['event_id']
        event = Event.objects.get(pk=event_id)
        print(event)
        print(event.event_name)

        # form = ParticipationForm(request.POST)
        # print('Printing the current user... ', user)
        # if form.is_valid():
        #     print('Form is valid. Saving form...')
        #     try:
        #         form.save()
        #         print("The team was saved in the database")
        #         return render(request, 'add_members.html', {'event': event, 'user': user})
        #     except:
        #         print("The team did not save in the database")
        #         pass
        # else:
        #     form = ParticipateForm()
        #     return render(request, 'participate.html', {'form': form, 'event': event})
        return render(request, 'participate.html', {'event': event})
