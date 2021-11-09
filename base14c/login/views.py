from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .form import CreerUtilisateur
from django.contrib import messages


# Create your views here.

def InscriptionPage(request):
    form = CreerUtilisateur()
    if request.method == 'POST':
        form = CreerUtilisateur(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account successfully created')
            return redirect('sample/')
    context = {'form': form }
    return render(request, 'login/inscription.html', context)


def LoginPage(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('sample/')
        else:
            messages.info(request, 'Username or Password is incorrect')
    return render(request, 'login/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('/')

