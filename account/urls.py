from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('',myProfileCalendar,name="myProfileCalendar"),

    path('logout/',logtoout,name="logtoout"),
    path('login/',loggingin,name="loggingin"),

    path('register/',register,name="register"),
    path('settings/',mySettings,name="mySettings"),

    path('hashtag/toggle-like/<int:id>/', toggleHashtag, name='toggle_hashtag_like'),
    path('community/toggle-like/<int:id>/', toggleCommunity, name='toggle_community_like'),
    path('place/toggle-like/<int:id>/', togglePlace, name='toggle_place_like'),
    path('activity/toggle-like/<int:id>/', toggleActivity, name='toggle_activity_like'),

    path('w/1/',welcome1,name="welcome1"),
    path('w/2/',welcome2,name="welcome2"),
    path('w/3/',welcome3,name="welcome3"),
    path('w/4/',welcome4,name="welcome4"),
    path('w/5/',welcome5,name="welcome5"),
    path('w/6/',welcome6,name="welcome6"),


    path('api/login/', LoginAPIView.as_view(), name='api_login'),
    path('api/logout/', LogoutAPIView.as_view(), name='api_logout'),
    path('api/profile/', UserProfileView.as_view(), name='user-profile-view'),
    path('api/profile/<str:username>/', OtherUserProfileView.as_view(), name='other-user-profile'),
    
    path('api/register/', api_register, name='api_register'),
    path('api/is_logged_in/', is_logged_in, name='is_logged_in'),
    path('api/update_profile/', update_profile, name='update_profile'),
    path('api/forgot_password/', forgot_password, name='forgot_password'),
    path('api/save_fbmtoken/', save_fbmtoken, name='save_token'),
    


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
