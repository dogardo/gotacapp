from django.contrib import admin
from .models import *

@admin.register(activities)
class activity_panel(admin.ModelAdmin):

    list_display=["id","name"] #paneli özelleştiren
    list_display_links=["id","name"]  #basmalı yapan
    search_fields=["name","id"] #arama çubuğu oluşturan
    list_filter= ["name","id"] #sağda panel oluşturan
    
    class Meta:
        model=activities

@admin.register(places)
class activity_panel(admin.ModelAdmin):

    list_display=["id","name"] #paneli özelleştiren
    list_display_links=["id","name"]  #basmalı yapan
    search_fields=["name","id"] #arama çubuğu oluşturan
    list_filter= ["name","id"] #sağda panel oluşturan
    
    class Meta:
        model=places

@admin.register(hashtags)
class activity_panel(admin.ModelAdmin):

    list_display=["id","name"] #paneli özelleştiren
    list_display_links=["id","name"]  #basmalı yapan
    search_fields=["name","id"] #arama çubuğu oluşturan
    list_filter= ["name","id"] #sağda panel oluşturan
    
    class Meta:
        model=hashtags

@admin.register(communities)
class activity_panel(admin.ModelAdmin):

    list_display=["id","name"] #paneli özelleştiren
    list_display_links=["id","name"]  #basmalı yapan
    search_fields=["name","id"] #arama çubuğu oluşturan
    list_filter= ["name","id"] #sağda panel oluşturan
    
    class Meta:
        model=communities