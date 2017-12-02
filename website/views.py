from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from website.forms import LoginForm
from website.forms import RegisterForm
import hashlib
import random
import uuid
import time
from website.models import *


# Create your views here.
sessions = {}
logged_in = {}
timeout = 2700

def index(request):
    template = loader.get_template('login.html')
    context = {"loginform": LoginForm(),
               "registerform": RegisterForm(), }
    return HttpResponse(template.render(context, request))



def login_user(username):

    if username in logged_in:
        if logged_in[username][1] < 2700:
            return HttpResponseRedirect("/home/" + logged_in[username][0] + "/")
        else:
            del logged_in[username]

    session_key = str(uuid.uuid4())
    logged_in[username] = (session_key,(time.time() * 1000000))
    sessions[session_key] = username

    return HttpResponseRedirect("/home/" + session_key + "/")


def respond_login(request):
    def fail_login(request):
        template = loader.get_template('login.html')
        context = {"loginform": LoginForm(),
                   "registerform": RegisterForm(),
                   "login_err_mesg": "Error: incorrect username or password"}

        return HttpResponse(template.render(context, request))

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = str(form.cleaned_data['password'])

            # num_results = User.objects.filter(account_name=username).count()

            # gets the first and only value
            results = list(User.objects.raw("SELECT * from users where account_name = %s", [username]))
            if len(results) == 0:
                return fail_login(request)

            result = results[0]
            salt = result.password_salt

            combined = str.encode(salt + password)
            passhash = hashlib.sha256(combined).hexdigest()

            if passhash == result.password_hash:
                return login_user(username)

            return fail_login()
            # return HttpResponseRedirect("/home/")

    return HttpResponse("Failed: This link is for post requests")


def respond_register(request):
    def register_fail(request, message):
        template = loader.get_template('login.html')
        context = {"loginform": LoginForm(),
                   "registerform": RegisterForm(),
                   "register_err_mesg": "Error: " + message + " "}

        return HttpResponse(template.render(context, request))

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            salt = ''.join(list(map(chr, [random.randint(97, 122) for i in range(7)])))

            password = str(form.cleaned_data['password'])
            if password != str(form.cleaned_data['confirm_password']):
                return register_fail(request, "passwords must match")

            combined = str.encode(salt + password)
            passhash = hashlib.sha256(combined).hexdigest()

            # num_results = User.objects.filter(account_name=username).count()


            num_results = len(list(User.objects.raw("SELECT * from users where account_name = %s", [username])))
            if num_results > 0:
                return register_fail(request,"User already exists")

            new_user = User(account_name=form.cleaned_data['username'], password_hash=passhash, password_salt=salt)
            new_user.save()

            return login_user(username)
            # return HttpResponseRedirect("/home/")

    return HttpResponse("Error: This link is for post requests")


def homepage(request, session_id):
    def fail_session():
        template = loader.get_template('login.html')
        context = {"loginform": LoginForm(),
                   "registerform": RegisterForm(),
                   "login_err_mesg": "Error: invalid session id"}

        return HttpResponse(template.render(context, request))

    if session_id not in sessions:
        return fail_session()

    template = loader.get_template('homepage.html')
    for i in sessions:
        print(i, sessions[i])
    characters = Character.objects.raw("SELECT * FROM characters WHERE user_name_id = %s",[sessions[session_id]])
    context = {"characters": characters,
               "username": sessions[session_id]}
    return HttpResponse(template.render(context, request))