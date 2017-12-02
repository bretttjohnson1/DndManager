from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import website.global_functions as global_functions
# Create your views here.
def index(request):
    template = loader.get_template('test.html')
    context = {"list": ["a","bc","def"]}
    return HttpResponse(template.render(context, request))

def hello2(request):
    print(global_functions.global_path_to_local_path("html_docs/test.html"))
    return render(request, global_functions.global_path_to_local_path("html_docs/test.html"), {"list": ["a","bc","def"]})
