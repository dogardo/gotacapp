from rest_framework import serializers
from activities.models import hashtags, communities, places, activities
from django.conf import settings
from django.utils import timezone
from datetime import datetime

class HashtagsSerializer(serializers.ModelSerializer):
    pic_url = serializers.SerializerMethodField()
    user_wants_to_know = serializers.SerializerMethodField()  # Yeni alan

    class Meta:
        model = hashtags
        fields = ('id', 'name', 'pic', 'pic_url', 'user_wants_to_know')  # 'user_wants_to_know' ekledik

    def get_pic_url(self, obj):
        if obj.pic:
            return f"http://10.0.2.2:8000/{obj.pic.url}"
        return None

    def get_user_wants_to_know(self, obj):
        user = self.context.get('user')  # Kullanıcıyı context'ten al
        if user:
            return obj in user.wantToKnowHash.all()  # Bu hashtag'in kullanıcının "bilmek istediği" hashtag'ler arasında olup olmadığını kontrol et
        return False
    
class PlacesSerializer(serializers.ModelSerializer):
    pic_url = serializers.SerializerMethodField()
    user_wants_to_know = serializers.SerializerMethodField()

    class Meta:
        model = places
        fields = ('id', 'name', 'pic', 'pic_url', 'user_wants_to_know')

    def get_pic_url(self, obj):
        if obj.pic:
            return f"http://10.0.2.2:8000/{obj.pic.url}"
        return None

    def get_user_wants_to_know(self, obj):
        user = self.context.get('user')
        if user:
            return obj in user.wantToKnowPlac.all()
        return False

class CommunitiesSerializer(serializers.ModelSerializer):
    pic_url = serializers.SerializerMethodField()
    user_wants_to_know = serializers.SerializerMethodField()

    class Meta:
        model = communities
        fields = ('id', 'name', 'pic', 'pic_url', 'user_wants_to_know')

    def get_pic_url(self, obj):
        if obj.pic:
            return f"http://10.0.2.2:8000/{obj.pic.url}"
        return None

    def get_user_wants_to_know(self, obj):
        user = self.context.get('user')
        if user:
            return obj in user.wantToKnowComm.all()
        return False

class ActivitiesSerializer(serializers.ModelSerializer):

    hashtag_pic_url = serializers.SerializerMethodField()
    place_pic_url = serializers.SerializerMethodField()
    community_pic_url = serializers.SerializerMethodField()
    user_wants_to_know = serializers.SerializerMethodField()
    hashtag_name = serializers.SerializerMethodField()
    place_name = serializers.SerializerMethodField()
    community_name = serializers.SerializerMethodField()
    formatted_m_time = serializers.SerializerMethodField()

    class Meta:
        model = activities
        fields = (
            'id', 'name', 'description',
            'hashtag', 'hashtag_pic_url', 'hashtag_name',
            'place', 'place_pic_url', 'place_name',
            'community', 'community_pic_url', 'community_name',
            'm_time', 'formatted_m_time', 'creator',
            'activity', 'user_wants_to_know'
        )

    def get_hashtag_pic_url(self, obj):
        if obj.hashtag and obj.hashtag.pic:
            return f"http://10.0.2.2:8000/{obj.hashtag.pic.url}"
        return None

    def get_place_pic_url(self, obj):
        if obj.place and obj.place.pic:
            return f"http://10.0.2.2:8000/{obj.place.pic.url}"
        return None

    def get_community_pic_url(self, obj):
        if obj.community and obj.community.pic:
            return f"http://10.0.2.2:8000/{obj.community.pic.url}"
        return None
    
    def get_hashtag_name(self, obj):
        return obj.hashtag.name if obj.hashtag else None

    def get_place_name(self, obj):
        return obj.place.name if obj.place else None

    def get_community_name(self, obj):
        return obj.community.name if obj.community else None

    def get_formatted_m_time(self, obj):
        if obj.m_time:
            # m_time'ı yerel zaman dilimine çevir (eğer gerekliyse)
            local_time = timezone.localtime(obj.m_time)
            return local_time.strftime("%d/%m/%Y %H:%M")
        return None
    
    def get_user_wants_to_know(self, obj):
        user = self.context.get('user')
        if user:
            return obj in user.IKnowAct.all()
        return False
    

class HashtagsInfo(serializers.ModelSerializer):
    class Meta:
        model = hashtags
        fields = '__all__'

class PlacesInfo(serializers.ModelSerializer):
    class Meta:
        model = places
        fields = '__all__'

class CommunitiesInfo(serializers.ModelSerializer):
    class Meta:
        model = communities
        fields = '__all__'