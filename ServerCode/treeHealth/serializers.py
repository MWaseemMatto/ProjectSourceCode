from rest_framework import serializers
from .models import User,  MobileImages


class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = ('name', 'field_of_interest', 'organization')
        fields = '__all__'



class MobileImagesSerializer (serializers.ModelSerializer):
    class Meta:
        model = MobileImages
        fields = '__all__'
