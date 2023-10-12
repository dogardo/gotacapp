from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
import datetime 
from account.forms import *
from account.models import *
from activities.models import *
from activities.views import *
from activities.forms import *
from activities.urls import *
from activities.urls import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .forms import *
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
import random
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import usercore
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ForgotPasswordSerializer
import random
import string
import os
import logging
logger = logging.getLogger(__name__)

def loggingin(request): #yarım

    form = loginForm(request.POST, request.FILES or None)
    if request.method == "POST" and form.is_valid():

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user_existence =  authenticate(username = username,password=password)  

        if user_existence:
            login(request,user_existence)
            if request.user.firstLogin == True:
                return redirect("welcome1")
            else:
                messages.success(request,"Kullanıcı girişi başarıyla tamamlandı.")
                return redirect("myProfileCalendar")

        else:
            messages.warning(request,"Kullanıcı adı ya da şifre hatalı.")

    values = {
        "form":form,
    }
    
    return render(request,"account/login.html",values)

@login_required(login_url='index')
def logtoout(request):

    logout(request)
    messages.success(request,"Çıkış başarıyla tamamlandı...")
    return redirect("index")

@login_required(login_url='index')
def mySettings(request): 
    user = usercore.objects.get(id=request.user.id)
    form = updateForm(request.POST, request.FILES or None)

    if request.method == "POST":

        if form.is_valid():

            password = form.cleaned_data.get("password")
            email = form.cleaned_data.get("email")
            phone = form.cleaned_data.get("phone")
            pic1 = form.cleaned_data.get("pic1")

            if pic1:
                print("1")
                user.pic1 = pic1
                user.save()

            if password:
                print("2")
                new_password = make_password(password)
                user.password = new_password
                user.save()

            if email:
                print("3")
                user.email = email
                user.save()

            if phone:
                print("4")
                user.phone = phone
                user.save()

            messages.success(request,"Veriler Yenilendi")
        else:
            messages.success(request,"Hata sonucu, veriler yenilenemedi.")


    values = {
        "user":user,
        "form":form,
    }

   
    return render(request,"account/settings.html",values)
    
def register(request): #yarım

    form = registerForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            name = form.cleaned_data.get("name")
            email = form.cleaned_data.get("email")
            phone = form.cleaned_data.get("phone")
            gender = form.cleaned_data.get("gender")

            newUsercore = usercore(username=username,password=password,name=name,email=email,
                                phone=phone,gender=gender)
            
            newUsercore.set_password(password)
            newUsercore.save()

            messages.success(request,"Hesabınız Oluşturuldu, Tanıtım Sekmesindesiniz. Tanıtım Sekmelerini Uygun Şekilde Geçerek, Hesabınızı Aktive Edebilirsiniz.")

            user_existence =  authenticate(username = username,password=password)  

            if user_existence:
                login(request,user_existence)

                if request.user.firstLogin == True:

                    return redirect("welcome1")
                else:
                    return redirect("myProfileCalendar")
                
            else:
                messages.success(request,"Hesap Oluşturuldu, Giriş Yapabilirsiniz..")
                return render(request,"account/login.html")
        else:
            messages.success(request,"Hesap Oluşturulamadı, Türkçe Karakter Kullanmayınız.")

    values = {
        "form":form,
    }

    return render(request,"account/register.html",values)

@login_required(login_url='index')
def toggleHashtag(request, id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        user = get_object_or_404(usercore, id=request.user.id)
        hashtag = get_object_or_404(hashtags, id=id)

        if hashtag in user.wantToKnowHash.all():
            user.wantToKnowHash.remove(hashtag)
            is_added = False
            message = 'Başarıyla kaldırıldı'
        else:
            user.wantToKnowHash.add(hashtag)
            is_added = True
            message = 'Başarıyla kaydedildi'

        user.save()
        return JsonResponse({'success': True, 'is_added': is_added, 'message': message})
    else:
        return JsonResponse({'success': False, 'message': 'Geçersiz istek'})

@login_required(login_url='index')
def toggleCommunity(request, id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        user = get_object_or_404(usercore, id=request.user.id)
        community = get_object_or_404(communities, id=id)

        if community in user.wantToKnowComm.all():
            user.wantToKnowComm.remove(community)
            is_added = False
            message = 'Başarıyla kaldırıldı'
        else:
            user.wantToKnowComm.add(community)
            is_added = True
            message = 'Başarıyla kaydedildi'

        user.save()
        return JsonResponse({'success': True, 'is_added': is_added, 'message': message})
    else:
        return JsonResponse({'success': False, 'message': 'Geçersiz istek'})

@login_required(login_url='index')
def togglePlace(request, id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        user = get_object_or_404(usercore, id=request.user.id)
        place = get_object_or_404(places, id=id)

        if place in user.wantToKnowPlac.all():
            user.wantToKnowPlac.remove(place)
            is_added = False
            message = 'Başarıyla kaldırıldı'
        else:
            user.wantToKnowPlac.add(place)
            is_added = True
            message = 'Başarıyla kaydedildi'

        user.save()
        return JsonResponse({'success': True, 'is_added': is_added, 'message': message})
    else:
        return JsonResponse({'success': False, 'message': 'Geçersiz istek'})
    
@login_required(login_url='index')
def toggleActivity(request, id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        user = get_object_or_404(usercore, id=request.user.id)
        activity = get_object_or_404(activities, id=id)

        if activity in user.IKnowAct.all():
            user.IKnowAct.remove(activity)
            is_added = False
            message = 'Başarıyla kaldırıldı'
        else:
            user.IKnowAct.add(activity)
            is_added = True
            message = 'Başarıyla kaydedildi'

        user.save()
        return JsonResponse({'success': True, 'is_added': is_added, 'message': message})
    else:
        return JsonResponse({'success': False, 'message': 'Geçersiz istek'})
    
@login_required(login_url='index')
def myProfileCalendar(request):
    user = usercore.objects.get(id=request.user.id)
    today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)

    try:
        filteredKnowAct = [value for value in user.IKnowAct.all() if value.m_time > today]
        filteredKnowAct = sorted(filteredKnowAct, key=lambda x: x.m_time)
    except:
        pass

    try:
        communities = [value for value in user.wantToKnowComm.all()]
        shuffledCommunities = list(communities)
        random.shuffle(shuffledCommunities)
    except:
        pass

    try:
        hashtags = [value for value in user.wantToKnowHash.all()]
        shuffledHashtags = list(hashtags)
        random.shuffle(shuffledHashtags)
    except:
        pass

    try:
        places = [value for value in user.wantToKnowPlac.all()]
        shuffledPlaces = list(places)
        random.shuffle(shuffledPlaces)
    except:
        pass

    try:
        filteredKnowActOld = [value for value in user.IKnowAct.all() if value.m_time < today]
        filteredKnowActOld = sorted(filteredKnowActOld, key=lambda x: x.m_time,reverse=True)

    except:
        pass

    values={
        "user":user,
        "filteredKnowAct":filteredKnowAct,
        "shuffledPlaces":shuffledPlaces,
        "shuffledCommunities":shuffledCommunities,
        "shuffledHashtags":shuffledHashtags,
        "filteredKnowActOld":filteredKnowActOld,
    }

    return render(request,"account/calendar.html",values)

@login_required(login_url='index')
def welcome1(request):

    allhashtags = hashtags.objects.all()

    allhashtags = list(allhashtags)

    random.shuffle(allhashtags)

    values= {
        "hashtags":allhashtags,
    }

    return render(request,"account/first/hashtags.html",values)

@login_required(login_url='index')
def welcome2(request):

    allcommunities = communities.objects.all()

    allcommunities = list(allcommunities)

    random.shuffle(allcommunities)

    values= {
        "communities":allcommunities,
    }

    return render(request,"account/first/communities.html",values)

@login_required(login_url='index')
def welcome3(request):

    allplaces = places.objects.all()

    allplaces  = list(allplaces)

    random.shuffle(allplaces)

    values= {
        "places":allplaces,
    }

    return render(request,"account/first/places.html",values)

@login_required(login_url='index')
def welcome4(request):

    user = usercore.objects.get(id=request.user.id)
    today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)

    try:

        filteredHash = [value for value in activities.objects.all() if value.hashtag in user.wantToKnowHash.all()]
        filteredComm = [value for value in activities.objects.all() if value.community in user.wantToKnowComm.all()]

        filteredActs = filteredComm + filteredHash

        filteredActs_set = set(filteredActs)

        filteredActs = list(filteredActs_set)

        filteredActs = [value for value in filteredActs if value.m_time > today]
        filteredActs = sorted(filteredActs, key=lambda x: x.m_time)

        filteredActs = [value for value in filteredActs if value.place in user.wantToKnowPlac.all()]
        
    except:
        pass

    values= {
        "activities":filteredActs,
    }

    return render(request,"account/first/activities.html",values)

@login_required(login_url='index')
def welcome5(request):
    user = usercore.objects.get(id=request.user.id)
    today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)

    try:
        filteredKnowAct = [value for value in user.IKnowAct.all() if value.m_time > today]
        filteredKnowAct = sorted(filteredKnowAct, key=lambda x: x.m_time)
    except:
        pass

    try:
        communities = [value for value in user.wantToKnowComm.all()]
        shuffledCommunities = list(communities)
        random.shuffle(shuffledCommunities)
    except:
        pass

    try:
        hashtags = [value for value in user.wantToKnowHash.all()]
        shuffledHashtags = list(hashtags)
        random.shuffle(shuffledHashtags)
    except:
        pass

    try:
        places = [value for value in user.wantToKnowPlac.all()]
        shuffledPlaces = list(places)
        random.shuffle(shuffledPlaces)
    except:
        pass

    try:
        filteredKnowActOld = [value for value in user.IKnowAct.all() if value.m_time > today]
        filteredKnowActOld = sorted(filteredKnowActOld, key=lambda x: x.m_time,reverse=True)
    except:
        pass

    values={
        "user":user,
        "filteredKnowAct":filteredKnowAct,
        "shuffledPlaces":shuffledPlaces,
        "shuffledCommunities":shuffledCommunities,
        "shuffledHashtags":shuffledHashtags,
        "filteredKnowActOld":filteredKnowActOld,
    }

    return render(request,"account/first/profile.html",values)

@login_required(login_url='index')
def welcome6(request):

    user = usercore.objects.get(id=request.user.id)
    user.firstLogin = False
    user.save()

    messages.success(request,"Aktivasyon Gerçekleşti.")
    return redirect("myProfileCalendar")

###APİ####################################

class LogoutAPIView(APIView):

    permission_classes = [IsAuthenticated]
    def post(self, request):
        if Token.objects.get(user=request.user):
            token = Token.objects.get(user=request.user)
            token.delete()
            request.user.firebase_messaging_token = None
            request.user.save()

        logout(request)
        return Response({"message": "Çıkış başarıyla tamamlandı...",'isLoggedIn':False}, status=status.HTTP_200_OK,content_type="application/json; charset=utf-8")
    
class LoginAPIView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user_existence = authenticate(username=username, password=password)
            
            if user_existence:
                login(request, user_existence)
                token, created = Token.objects.get_or_create(user=user_existence)
                if request.user.firstLogin:
                    return Response({"token": token.key,"isLoggedIn":True}, status=status.HTTP_200_OK)
                else:
                    return Response({"token": token.key,"isLoggedIn":True}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Kullanıcı adı ya da şifre hatalı."}, status=status.HTTP_401_UNAUTHORIZED,content_type="application/json; charset=utf-8")
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):

    def get(self, request, format=None):
        user = request.user  # Oturum açmış kullanıcıyı al
        serializer = UserProfileSerializer(user)  # Serializer kullanarak veriyi hazırla
        return Response(serializer.data,content_type="application/json; charset=utf-8")  # Hazırlanan veriyi yanıt olarak gönder

class OtherUserProfileView(APIView):

    def get(self, request, username, format=None):
        try:
            user = usercore.objects.get(username=username)  # Kullanıcı adını kullanarak kullanıcıyı al
        except usercore.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(user)  # Serializer kullanarak veriyi hazırla
        return Response(serializer.data, content_type="application/json; charset=utf-8")
      
@api_view(['POST'])
def api_register(request):

    serializer = RegisterUserSerializer(data=request.data)
    
    if serializer.is_valid():
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        confirm = serializer.validated_data["confirm"]
        name = serializer.validated_data["name"]
        email = serializer.validated_data["email"]
        phone = serializer.validated_data["phone"]
        gender = serializer.validated_data["gender"]

        try:
            existing_username = usercore.objects.get(username=username)
            return Response({"message": "Bu kullanıcı adı zaten kayıtlı."}, status=400,content_type="application/json; charset=utf-8")
        except ObjectDoesNotExist:
            pass

        if password != confirm:
            return Response({"message": "Şifre ve doğrulama şifresi eşleşmiyor."}, status=400,content_type="application/json; charset=utf-8")

        try:
            existing_email = usercore.objects.get(email=email)
            return Response({"message": "Bu e-posta adresi zaten kayıtlı."}, status=400,content_type="application/json; charset=utf-8")
        except ObjectDoesNotExist:
            pass

        try:
            existing_phone = usercore.objects.get(phone=phone)
            return Response({"message": "Bu telefon numarası zaten kayıtlı"}, status=400,content_type="application/json; charset=utf-8")
        except ObjectDoesNotExist:
            pass

        try:
            x = len(phone)
            if x != 11:
                return Response({"message": "Telefon Numarasını 11 haneli haliyle yazınız (başına 90 ekleyiniz)"}, status=400,content_type="application/json; charset=utf-8")
        except:
            pass

        newUsercore = usercore(username=username, name=name, email=email, phone=phone, gender=gender)
        newUsercore.set_password(password)
        newUsercore.save()

        user_existence = authenticate(username=username, password=password)  

        if user_existence:
            login(request, user_existence)

            if user_existence.firstLogin == True:
                token, created = Token.objects.get_or_create(user=newUsercore)
                return Response({"message": "Hesabınız Oluşturuldu. Tanıtım Sekmesini Uygun Şekilde Geçerek, Hesabınızı Aktive Edebilirsiniz.","token": str(token)},content_type="application/json; charset=utf-8")

            return Response({"message": "Hesabınız Oluşturuldu.","token": str(token)},content_type="application/json; charset=utf-8")

        else:
            return Response({"message": "Hesap Oluşturuldu, Giriş Yapabilirsiniz.","token": str(token)}, status=201,content_type="application/json; charset=utf-8")

    return Response({"message": "Gönderilen Değerlerden Biri/Birkaçı Geçersiz ( + Türkçe Karakter Kullanmayınız.)" }, status=400 ,content_type="application/json; charset=utf-8")

def is_logged_in(request):
    response_data = {'is_logged_in': request.user.is_authenticated}
    return JsonResponse(response_data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    data = request.data.dict()

    try:
        profile = usercore.objects.get(username=user.username)

        for field in ['username', 'name', 'phone', 'email', 'password']:
            if not data.get(field):
                data[field] = getattr(profile, field)

        serializer = UserProfileSerializer(profile, data=data, partial=True)

        if serializer.is_valid():
            if 'password' in data:
                new_password = data['password']

                profile.set_password(new_password)
                profile.save()

            try:
                if data['username'] != profile.username:
                    if 'username' in data and usercore.objects.get(username=data['username']):
                        return Response({'error': 'Bu kullanıcı adı zaten kullanılmaktadır.'}, status=status.HTTP_400_BAD_REQUEST)
            except usercore.DoesNotExist:
                pass

            try:
                if data['phone'] != profile.phone:
                    if 'phone' in data and usercore.objects.get(phone=data['phone']):
                        return Response({'error': 'Bu telefon numarası zaten kayıtlıdır.'}, status=status.HTTP_400_BAD_REQUEST)
                    if 'phone' in data and len(data['phone']) != 12:
                        return Response({'error': 'Telefon numarası 12 haneli olmalıdır : 905xxxxxxxxx'}, status=status.HTTP_400_BAD_REQUEST)
            except usercore.DoesNotExist:
                pass

            try:
                if data['email'] != profile.email:
                    if 'email' in data and usercore.objects.get(email=data['email']):
                        return Response({'error': 'Bu mail adresi zaten kullanılmaktadır.'}, status=status.HTTP_400_BAD_REQUEST)
            except usercore.DoesNotExist:
                pass

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except usercore.DoesNotExist:
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def forgot_password(request):

    serializer = ForgotPasswordSerializer(data=request.data)
    if serializer.is_valid():
        print(os.getenv('EMAIL_HOST_PASSWORD'))
        print(os.getenv('EMAIL_HOST_USER'))
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        print(username)
        print(email)

        try:
            user = usercore.objects.get(username=username, email=email)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        characters = string.ascii_letters + string.digits  # Sadece büyük harf, küçük harf ve sayıları içerir
        new_password = ''.join(random.choice(characters) for _ in range(12))
        
        try:
            send_mail(
                'Your new password',
                f'Here is your new password: {new_password}',
                None,  # <-- Burası None olmamalı
                [email],
                fail_silently=False,
            )
        except Exception as e:
            print("E-posta gönderme hatası:", e)
            return Response({"error": f"Password reset failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # E-posta başarıyla gönderildiyse şifreyi güncelle
        user.set_password(new_password)
        user.save()
        
        return Response({"message": "New password has been sent to your email"}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_fbmtoken(request):
    if request.user.is_authenticated:
        token = request.POST.get('token')
        request.user.firebase_messaging_token = token
        request.user.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'unauthorized'}, status=401)