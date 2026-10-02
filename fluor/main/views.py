from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from .forms import *

# Create your views here.
def main_view(request):
    return HttpResponse("Пустышка")

class RegistrationUser(CreateView):
    form_class = RegistrationForm
    template_name = 'html/registration.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main')

class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'html/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

def logout_user(request):
    logout(request)
    return redirect('main')