from rest_framework import serializers
from activities.models import hashtags, communities, places, activities
from account.models import *
from rest_framework import serializers
from django.utils import timezone
from datetime import datetime
from activities.serializers import HashtagsSerializer,PlacesSerializer,CommunitiesSerializer,ActivitiesSerializer

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, style={'input_type': 'password'})

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = usercore
        fields = ['password', 'email', 'phone', 'pic1']

class UserSettingsSerializer(serializers.Serializer):
    password = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False)
    pic1 = serializers.ImageField(required=False)

class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(write_only=True)
    confirm = serializers.CharField(write_only=True)  # Şifre doğrulaması için
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=15)
    gender = serializers.CharField(max_length=10)

    def validate(self, data):
        password = data.get('password')
        confirm = data.get('confirm')

        if password != confirm:
            raise serializers.ValidationError({"confirm": "Şifre ve şifre doğrulama eşleşmiyor."},content_type="application/json; charset=utf-8")

        return data

class UserProfileSerializer(serializers.ModelSerializer):
    pic1_url = serializers.SerializerMethodField()  # Yeni alan
    wantToKnowHash = HashtagsSerializer(many=True, read_only=True)
    wantToKnowComm = CommunitiesSerializer(many=True, read_only=True)
    wantToKnowPlac = PlacesSerializer(many=True, read_only=True)
    IKnowAct = ActivitiesSerializer(many=True, read_only=True)

    class Meta:
        model = usercore
        fields = (
            'username', 'email', 'name', 'pic1', 'pic1_url',  # 'pic1_url' ekledik
            'wantToKnowHash', 'wantToKnowComm', 'wantToKnowPlac', 'IKnowAct',
            'firstLogin', 'gender', 'phone', 'date_joined',
        )

    def get_pic1_url(self, obj):
        if obj.pic1:
            return f"http://10.0.2.2:8000/{obj.pic1.url}"  # Sunucu URL'nizi buraya ekleyin
        return None
    
class UserProfileSerializer(serializers.ModelSerializer):
    pic1_url = serializers.SerializerMethodField()  # Yeni alan
    wantToKnowHash = HashtagsSerializer(many=True, read_only=True)
    wantToKnowComm = CommunitiesSerializer(many=True, read_only=True)
    wantToKnowPlac = PlacesSerializer(many=True, read_only=True)
    IKnowAct = ActivitiesSerializer(many=True, read_only=True)

    class Meta:
        model = usercore
        fields = (
            'username', 'email', 'name', 'pic1', 'pic1_url',  # 'pic1_url' ekledik
            'wantToKnowHash', 'wantToKnowComm', 'wantToKnowPlac', 'IKnowAct',
            'firstLogin', 'gender', 'phone', 'date_joined',
        )

    def get_pic1_url(self, obj):
        if obj.pic1:
            return f"http://10.0.2.2:8000/{obj.pic1.url}"  # Sunucu URL'nizi buraya ekleyin
        return None
        
class ForgotPasswordSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()