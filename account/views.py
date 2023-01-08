from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.models import Group

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            #crear un nuevo usuario
            new_user = user_form.save(commit=False)
            #nueva contrasena
            new_user.set_password(user_form.cleaned_data['password'])
            #guardar el nuevo usuario
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        
        return render(request, 'account/register.html', {'user_form':user_form})
    
def profile(request, user_id, username):
    user = get_object_or_404(User, id=user_id, username=username)
    profile = get_object_or_404(Profile, user=user)
    context = {'user':user, 'profile':profile}
    return render(request, 'account/profile/profile.html', context)