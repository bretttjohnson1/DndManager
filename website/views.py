from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from website.forms import LoginForm
from website.forms import RegisterForm
# Create your views here.


def index(request):
    template = loader.get_template('login.html')
    context = {"loginform": LoginForm(),
               "registerform": RegisterForm(),}
    return HttpResponse(template.render(context, request))


def respond_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            print("worked")
            return HttpResponse("<h1>login</h1>")
            return HttpResponseRedirect("/home/")
    return HttpResponse("Failed")


def respond_register(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            print("worked")
            return HttpResponse("<h1>login</h1>")
            return HttpResponseRedirect("/home/")
    return HttpResponse("Failed")