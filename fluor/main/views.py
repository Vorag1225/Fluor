from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def main_view(request):
    return HttpResponse("Пустышка")
def registration_view(request):
    return render(request, "html/registration.html")