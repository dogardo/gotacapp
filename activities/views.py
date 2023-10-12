from django.shortcuts import render
from account.models import *
from activities.models import *
import random
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
def allhashtags(request):

    allhashtags = hashtags.objects.all()

    allhashtags = list(allhashtags)

    random.shuffle(allhashtags)

    values= {
        "hashtags":allhashtags,
    }

    return render(request,"activities/hashtags.html",values)

def allcommunities(request):

    allcommunities = communities.objects.all()

    allcommunities = list(allcommunities)

    random.shuffle(allcommunities)

    values= {
        "communities":allcommunities,
    }

    return render(request,"activities/communities.html",values)

def allplaces(request):

    allplaces = places.objects.all()

    allplaces  = list(allplaces)

    random.shuffle(allplaces)

    values= {
        "places":allplaces,
    }

    return render(request,"activities/places.html",values)

def allactivities(request):


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

    return render(request,"activities/activities.html",values)

######### API

@api_view(['GET'])
def all_hashtags_api(request):
    auth = TokenAuthentication()
    try:
        auth_result = auth.authenticate(request)
        if auth_result is not None:
            request.user = auth_result[0]
    except AuthenticationFailed:
        pass  # veya istediğiniz bir hatayı döndürebilirsiniz

    allhashtags_data = hashtags.objects.all()
    allhashtags = list(allhashtags_data)
    random.shuffle(allhashtags)
    serializer = HashtagsSerializer(allhashtags, many=True, context={'user': request.user})
    return Response(serializer.data,content_type="application/json; charset=utf-8")

@api_view(['GET'])
@login_required
def user_want_to_know_hashtags(request):
    token_key = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
    token = Token.objects.get(key=token_key)
    user = token.user
    want_to_know = user.wantToKnowHash.all()
    serializer = HashtagsSerializer(want_to_know, many=True)
    return Response(serializer.data,content_type="application/json; charset=utf-8")


@api_view(['GET'])
@login_required
def other_user_want_to_know_hashtags(request, username):
    try:
        other_user = usercore.objects.get(username=username)
    except usercore.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    want_to_know = other_user.wantToKnowHash.all()
    serializer = HashtagsSerializer(want_to_know, many=True)
    return Response(serializer.data, content_type="application/json; charset=utf-8")


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def toggle_hashtag(request):
    hashtag_id = request.data.get("hashtag_id")
    user = request.user

    try:
        hashtag = hashtags.objects.get(id=hashtag_id)
    except hashtags.DoesNotExist:
        return Response({"status": "error", "message": "Hashtag does not exist"}, status=400)

    if hashtag in user.wantToKnowHash.all():
        user.wantToKnowHash.remove(hashtag)
        action = "removed"
    else:
        user.wantToKnowHash.add(hashtag)
        action = "added"

    return Response({"status": "success", "action": action},status=200)

@api_view(['GET'])
def all_places_api(request):
    auth = TokenAuthentication()
    try:
        auth_result = auth.authenticate(request)
        if auth_result is not None:
            request.user = auth_result[0]
    except AuthenticationFailed:
        pass

    allplaces_data = places.objects.all()
    allplaces = list(allplaces_data)
    random.shuffle(allplaces)
    serializer = PlacesSerializer(allplaces, many=True, context={'user': request.user})
    return Response(serializer.data,content_type="application/json; charset=utf-8")

@api_view(['GET'])
@login_required
def user_want_to_know_places(request):
    token_key = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
    token = Token.objects.get(key=token_key)
    user = token.user
    want_to_know = user.wantToKnowPlac.all()
    serializer = PlacesSerializer(want_to_know, many=True)
    return Response(serializer.data,content_type="application/json; charset=utf-8")

@api_view(['GET'])
@login_required
def other_user_want_to_know_places(request, username):
    try:
        other_user = usercore.objects.get(username=username)
    except usercore.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    want_to_know = other_user.wantToKnowPlac.all()
    serializer = PlacesSerializer(want_to_know, many=True)
    return Response(serializer.data, content_type="application/json; charset=utf-8")

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def toggle_place(request):
    place_id = request.data.get("place_id")
    user = request.user

    try:
        place = places.objects.get(id=place_id)
    except places.DoesNotExist:
        return Response({"status": "error", "message": "Place does not exist"}, status=400)

    if place in user.wantToKnowPlac.all():
        user.wantToKnowPlac.remove(place)
        action = "removed"
    else:
        user.wantToKnowPlac.add(place)
        action = "added"

    return Response({"status": "success", "action": action}, status=200)

@api_view(['GET'])
def all_communities_api(request):
    auth = TokenAuthentication()
    try:
        auth_result = auth.authenticate(request)
        if auth_result is not None:
            request.user = auth_result[0]
    except AuthenticationFailed:
        pass  # veya istediğiniz bir hatayı döndürebilirsiniz

    allcommunities_data = communities.objects.all()
    allcommunities = list(allcommunities_data)
    random.shuffle(allcommunities)
    serializer = CommunitiesSerializer(allcommunities, many=True, context={'user': request.user})
    return Response(serializer.data,content_type="application/json; charset=utf-8")

@api_view(['GET'])
@login_required
def user_want_to_know_communities(request):
    token_key = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
    token = Token.objects.get(key=token_key)
    user = token.user
    want_to_know = user.wantToKnowComm.all()
    serializer = CommunitiesSerializer(want_to_know, many=True)
    return Response(serializer.data,content_type="application/json; charset=utf-8")

@api_view(['GET'])
@login_required
def other_user_want_to_know_communities(request, username):
    try:
        other_user = usercore.objects.get(username=username)
    except usercore.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    want_to_know = other_user.wantToKnowComm.all()
    serializer = CommunitiesSerializer(want_to_know, many=True)
    return Response(serializer.data, content_type="application/json; charset=utf-8")

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def toggle_community(request):
    community_id = request.data.get("community_id")
    user = request.user

    try:
        community = communities.objects.get(id=community_id)
    except communities.DoesNotExist:
        return Response({"status": "error", "message": "Hashtag does not exist"}, status=400)

    if community in user.wantToKnowComm.all():
        user.wantToKnowComm.remove(community)
        action = "removed"
    else:
        user.wantToKnowComm.add(community)
        action = "added"

    return Response({"status": "success", "action": action},status=200)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def all_activities_api(request):

    token_key = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
    token = Token.objects.get(key=token_key)
    user = token.user
    today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    filteredActs = []

    try:

        filteredHash = [value for value in activities.objects.all() if value.hashtag in user.wantToKnowHash.all()]
        filteredComm = [value for value in activities.objects.all() if value.community in user.wantToKnowComm.all()]

        filteredActs = filteredComm + filteredHash

        filteredActs_set = set(filteredActs)

        filteredActs = list(filteredActs_set)

        filteredActs = [value for value in filteredActs if value.m_time > today]
        filteredActs = sorted(filteredActs, key=lambda x: x.m_time)

        filteredActs = [value for value in filteredActs if value.place in user.wantToKnowPlac.all()]
        
    except Exception as e:
        return Response({'error': str(e)}, status=400,content_type="application/json; charset=utf-8")

    if not filteredActs:
        return Response([], status=200,content_type="application/json; charset=utf-8")

    serializer = ActivitiesSerializer(filteredActs, many=True, context={'user': request.user})
    print(serializer.data)
    return Response(serializer.data,content_type="application/json; charset=utf-8")


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def all_activities_random_api(request):

    token_key = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
    token = Token.objects.get(key=token_key)
    user = token.user
    today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    filteredActs = []

    try:

        allActs = [value for value in activities.objects.all()]
        filteredHash = [value for value in activities.objects.all() if value.hashtag in user.wantToKnowHash.all()]
        filteredComm = [value for value in activities.objects.all() if value.community in user.wantToKnowComm.all()]

        filteredActs = filteredComm + filteredHash

        # filteredActs = allActs - filteredActs
        filteredActs = [act for act in allActs if act not in filteredActs]

        filteredActs_set = set(filteredActs)
        filteredActs = list(filteredActs_set)

        filteredActs = [value for value in filteredActs if value.m_time > today]
        filteredActs = sorted(filteredActs, key=lambda x: x.m_time)

        filteredActs = [value for value in filteredActs if value.place in user.wantToKnowPlac.all()]

        if len(filteredActs) >= 4:
            filteredActs = random.sample(filteredActs, 4)
        else:
            filteredActs = filteredActs
        
    except Exception as e:
        return Response({'error': str(e)}, status=400,content_type="application/json; charset=utf-8")

    if not filteredActs:
        return Response([], status=200,content_type="application/json; charset=utf-8")

    serializer = ActivitiesSerializer(filteredActs, many=True, context={'user': request.user})
    print(serializer.data)
    return Response(serializer.data,content_type="application/json; charset=utf-8")

@api_view(['GET'])
@login_required
def user_want_to_know_activities(request):
    token_key = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
    token = Token.objects.get(key=token_key)
    user = token.user
    now = datetime.now()
    want_to_know = user.IKnowAct.all().filter(m_time__gte=now)
    serializer = ActivitiesSerializer(want_to_know, many=True)
    return Response(serializer.data,content_type="application/json; charset=utf-8")

@api_view(['GET'])
@login_required
def user_want_to_know_activities_old(request):
    token_key = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
    token = Token.objects.get(key=token_key)
    user = token.user
    now = datetime.now()
    want_to_know = user.IKnowAct.all().filter(m_time__lte=now)
    serializer = ActivitiesSerializer(want_to_know, many=True)
    return Response(serializer.data,content_type="application/json; charset=utf-8")

@api_view(['GET'])
@login_required
def other_user_want_to_know_activities_old(request, username):
    try:
        other_user = usercore.objects.get(username=username)
    except usercore.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    
    now = datetime.now()
    want_to_know = other_user.IKnowAct.all().filter(m_time__lte=now)
    serializer = ActivitiesSerializer(want_to_know, many=True)
    return Response(serializer.data, content_type="application/json; charset=utf-8")

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def toggle_activity(request):
    activity_id = request.data.get("activity_id")
    user = request.user

    try:
        activity = activities.objects.get(id=activity_id)
    except activities.DoesNotExist:
        return Response({"status": "error", "message": "Activity does not exist"}, status=400)

    if activity in user.IKnowAct.all():
        user.IKnowAct.remove(activity)
        action = "removed"
    else:
        user.IKnowAct.add(activity)
        action = "added"

    return Response({"status": "success", "action": action}, status=200)

@api_view(['POST'])
def create_activity(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        # Kullanıcıyı kimlik doğrula
        user = authenticate(username=username, password=password)

        # Kullanıcı kimlik doğrulandı mı ve admin mi?
        if user is not None and user.is_admin:
            try:
                # Model örneklerini alın
                hashtag_instance = hashtags.objects.get(name=request.data['hashtag'])
                place_instance = places.objects.get(name=request.data['place'])
                community_instance = communities.objects.get(name=request.data['community'])
                creator_instance = usercore.objects.get(username=request.data['creator'])

                # Aynı değerlere sahip bir activity olup olmadığını kontrol et
                existing_activity = activities.objects.get(
                    name=request.data['name'],
                    description=request.data['description'],
                    hashtag=hashtag_instance,
                    place=place_instance,
                    community=community_instance,
                    m_time=request.data['m_time'],
                    creator=creator_instance,
                    activity=request.data['activity']
                )
                return Response({"message": "Activity already exists"}, status=200)
            except ObjectDoesNotExist:
                # Yeni bir activity oluşturun
                new_activity = activities.objects.create(
                    name=request.data['name'],
                    description=request.data['description'],
                    hashtag=hashtag_instance,
                    place=place_instance,
                    community=community_instance,
                    m_time=request.data['m_time'],
                    creator=creator_instance,
                    activity=request.data['activity']
                )
                new_activity.save()
                return Response({"message": "Activity created"}, status=201)
            except Exception as e:
                return Response({"message": f"An error occurred: {str(e)}"}, status=500)
        else:
            return Response({"message": "Unauthorized"}, status=401)