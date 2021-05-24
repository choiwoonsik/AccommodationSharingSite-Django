from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from . import models

# Create your views here.


def index(request):
    return render(request, 'copyrights/copyright.html', {})
