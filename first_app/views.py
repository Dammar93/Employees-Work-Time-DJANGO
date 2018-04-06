from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from faker import Faker
fake = Faker()
from first_app.zestaw1 import zestaw1
from first_app.zestaw2 import zestaw2
from first_app.zestaw3 import zestaw3

# Our original index view function
# Corresponds to original_index.html (rename it to index.html to use it!)

# def index(request):
#     my_dict = {'insert_me':"Now I am coming from first_app/index.html!"}
#     # Make sure this is pointing to the correct index
#     return render(request,'first_app/index.html',context=my_dict)


def z1(request):
    return zestaw1(request)

def z2(request):
    return zestaw2(request)

def z3(request):
    return zestaw3(request)
