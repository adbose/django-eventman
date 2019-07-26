from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from events.forms import ParticipationForm
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

    # def get(self, request):
    #     form = ParticipationForm(request.GET)
    #     event_id = request.session['event_id']
    #     event = Event.objects.get(pk=event_id)
    #     print('Participation form opened using GET request')
    #     print('Printing the user... ', request.user)
    #     print('Printing the Event name... ', event.event_name)
    #
    #     return render(request, 'participate.html', {'form': form, 'event': event})

    def post(self, request):
        form = ParticipationForm(request.GET)
        print('Printing the empty form data from get...\n', form.data)

        form = ParticipationForm(request.POST)
        print('Participation form with POST request data...\n', form.data)

        event_id = request.session['event_id']
        event = Event.objects.get(pk=event_id)

        if form.is_valid():
            print("Form is valid")
            try:
                obj = form.save(commit=False)
                obj.event = event
                obj.save()
                print("The participating team was saved in the database")

                return redirect('/add_members')
            except:
                    print("The participating team did not save in the database")
                    pass
        else:
            form = ParticipationForm()

        return render(request, 'participate.html', {'form': form, 'event': event})
