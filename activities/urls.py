from django.contrib import admin
from django.urls import path
from .views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('',allactivities,name="allactivities"),
    path('hashtag/',allhashtags,name="allhashtags"),
    path('community/',allcommunities,name="allcommunities"),
    path('place/',allplaces,name="allplaces"),

    path('api/all_hashtags/', all_hashtags_api, name='all-hashtags-api'),
    path('api/user_want_to_know_hashtags/', user_want_to_know_hashtags, name='user_want_to_know_hashtags'),
    path('api/toggle_hashtag/', toggle_hashtag, name='toggle_hashtag'),

    path('api/<str:username>/user_want_to_know_hashtags/', other_user_want_to_know_hashtags, name='other_user_want_to_know_hashtags'),
    path('api/<str:username>/user_want_to_know_places/', other_user_want_to_know_places, name='other_user_want_to_know_places'),
    path('api/<str:username>/user_want_to_know_communities/', other_user_want_to_know_communities, name='other_user_want_to_know_communities'),
    path('api/<str:username>/user_want_to_know_activities_old/', other_user_want_to_know_activities_old, name='other_user_want_to_know_activities_old'),

    path('api/all_places/', all_places_api, name='all-places-api'),
    path('api/user_want_to_know_places/', user_want_to_know_places, name='user_want_to_know_places'),
    path('api/toggle_place/', toggle_place, name='toggle_place'),

    path('api/all_communities/', all_communities_api, name='all-communities-api'),
    path('api/user_want_to_know_communities/', user_want_to_know_communities, name='user_want_to_know_communities'),
    path('api/toggle_community/', toggle_community, name='toggle_community'),

    path('api/all_activities/', all_activities_api, name='all-activities-api-view'),  
    path('api/all_activities/random/', all_activities_random_api, name='all-activities-random-api-view'),  
    path('api/user_want_to_know_activities/', user_want_to_know_activities, name='user_want_to_know_activities'),
    path('api/user_want_to_know_activities_old/', user_want_to_know_activities_old, name='user_want_to_know_activities_old'),
    path('api/toggle_activity/', toggle_activity, name='toggle_activity'),
   
    path('api/loggercreate/', create_activity, name='create_activity'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
