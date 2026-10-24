from django.contrib.auth.decorators import login_required
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
@login_required
def main_view(request):
    posts = Post.objects.all().order_by('-created_at')

    context = {
        'current_page': 'feed',
        'posts': posts
    }

    return render(request, 'html/feed.html', context)

@login_required
def post_view(request, id):
    post = get_object_or_404(Post, id=id)

    context = {
        'current_page': 'post',
        'post': post
    }

    return render(request, 'html/post.html', context)

class RegistrationUser(CreateView):
    form_class = RegistrationForm
    template_name = 'html/registration.html'

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
    template_name = 'html/login.html'
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        context['current_page'] = 'login'
        return context

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request, id):
    user = get_object_or_404(User, id=id)
    posts = Post.objects.filter(author=user).order_by('-created_at')
    context = {
        'current_page': 'profile',
        'user': user,
        'posts': posts
    }
    return render(request, 'html/profile.html', context)

def error_404_view(request, exception):
    context = {
        'current_page': 'error',
        'message': 'Похоже, страница, которую вы ищете, не существует...',
        'error_code': '404 - Not Found',
    }

    return render(
        request,
        'html/error_page.html',
        status=404,
        context=context
    )