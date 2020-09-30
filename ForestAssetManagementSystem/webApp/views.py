from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
'''
from .models import User
from .models import UserImages
from .serializers import UserSerializer
from .serializers import UserImagesSerializer
'''
# Create your views here.


def homepage(request):
    return render(request, 'webApp/home.html')


def baseline(request):
    return render(request, 'webApp/baselineMaps.html')
