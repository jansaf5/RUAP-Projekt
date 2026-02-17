from django.shortcuts import render
from .forms import RegistrationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login
from django.urls import reverse
from .models import CustomUser

# Create your views here.
# views.py

def home(request):
    return render(request, 'health_app/home.html')

def RegisterView(request):
    context = {}

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password1']
            user.set_password(raw_password)                
            user.save()
            
            CustomUser.objects.create(
                user=user,
                username=user.username,
                password=user.password
            )


            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            if not form.errors:
                form.add_error(field=None, error='Passwords do not match.')
    else:
        form = RegistrationForm()
    context['form'] = form
    return render(request, 'accounts/register.html', context)

""""
from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'accounts/login.html')

def register(request):
    return render(request, 'accounts/register.html')  
    """  