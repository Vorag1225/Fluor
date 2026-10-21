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
    posts = Post.objects.all().order_by('-created_at')

    context = {
        'current_page': 'feed',
        'posts': posts
    }

    return render(request, 'html/app.html', context)

def post_view(request, id):
    post = get_object_or_404(Post, id=id)

    context = {
        'current_page': 'post',
        'post': post
    }

    return render(request, 'html/app.html', context)

class RegistrationUser(CreateView):
    form_class = RegistrationForm
    template_name = 'html/app.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        context['current_page'] = 'registration'
        return context

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        login(self.request, user)
        return redirect('main')

class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'html/app.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        context['current_page'] = 'login'
        return context

def logout_user(request):
    logout(request)
    next_page = request.GET.get('next')
    if not next_page:
        next_page = '/'
    return redirect(next_page)

def profile_view(request, id):
    user = get_object_or_404(User, id=id)
    posts = Post.objects.filter(author=user).order_by('-created_at')
    context = {
        'current_page': 'profile',
        'user': user,
        'posts': posts
    }
    return render(request, 'html/app.html', context)


def error_404_view(request, exception):
    context = {
        'current_page': 'error',
        'message': 'Похоже, страница, которую вы ищете, не существует...',
        'error_code': '404 - Not Found',
    }

    return render(
        request,
        'html/app.html',
        status=404,
        context=context
    )