from django.http import HttpResponse,Http404,JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.views.decorators.http import require_POST
from .forms import *
from .models import *
from .services import *
import json


# Create your views here.
def main_view(request):
    posts = Post.objects.all().order_by('-created_at')

    context = {
        'posts': posts
    }

    return render(request, 'html/feed.html', context)

def post_view(request, id):
    post = get_object_or_404(Post, id=id)

    context = {
        'post': post
    }

    return render(request, 'html/post.html', context)

class RegistrationUser(CreateView):
    form_class = RegistrationForm
    template_name = 'html/registration.html'

    def get_context_data(self, **kwargs):
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

def logout_user(request):
    logout(request)
    next_page = request.GET.get('next')
    if not next_page:
        next_page = '/'
    return redirect(next_page)

def profile_view(request, id):
    user = get_object_or_404(User, id=id)
    context = {
        'user': user
    }
    return render(request, 'html/profile.html', context)


def error_404_view(request, exception):
    context = {
        'message': 'Похоже, страница, которую вы ищете, не существует...',
        'error_code': '404 - Not Found',
    }

    return render(
        request,
        'html/error_page.html',
        status=404,
        context=context
    )

@require_POST
def vote_api(request,post_id):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"error":"Пользователь не авторизован"},
            status=401
        )
    try:
        data = json.loads(request.body)
    except:
        return JsonResponse(
            {"error":"Некорректный JSON"},
            status=400
        )
    value = data.get('value')
    if type(value) != int or value not in (-1,1):
        return JsonResponse(
            {"error":"Неправильное значение для value"},
            status=400
        )
    if not Post.objects.filter(id=post_id).exists():
        return JsonResponse(
            {"error":"Указанного поста не существует"},
            status=404
        )
    try:
        result = post_vote(
            post_id=post_id,
            user=request.user,
            value=value
        )
    except Exception as e:
        return JsonResponse(
            {"error": str(e)},
            status=400
        )
    return JsonResponse({
        "score": result["score"],
        "value": result["value"]
    })