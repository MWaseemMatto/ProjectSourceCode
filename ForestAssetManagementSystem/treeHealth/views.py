'''

CURRENTLY, NOT IN USE


'''

from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, MobileImages

from .serializers import UserSerializer,  MobileImagesSerializer


# Create your views here.
class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self):
        pass


class MobileImages(APIView):
    def get(self, request):
        mobile_images = MobileImages.objects.all()
        serializer = MobileImagesSerializer(mobile_images, many=True)
        return Response(serializer.data)

    def post(self):
        pass