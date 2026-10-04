from django.http import HttpResponse,Http404
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from .forms import *
from .models import *

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
        Profile.objects.create(user=user)
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

def profile_view(request,id):
    try:
        user = get_object_or_404(User, id=id)
        context = {
            'user': user
        }
        return render(request, 'html/profile.html',context)
    except ValueError:
        raise Http404("")

def error_404_view(request,exception):
    context = {
        'message':'Похоже, страница, которую вы ищете, не существует...',
        'error_code':'404 - Not Found',
    }
    return render(request,'html/error_page.html',status=404,context=context)