# from django.shortcuts import render
#
# # Create your views here.
#
# def index(request, *args, **kwargs):
#     return render(request, "frontend/index.html")
from django.shortcuts import render

def index(request):
    return render(request, "frontend/index.html")  # This is your React template
