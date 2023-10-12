from django.contrib import admin
from .models import *

@admin.register(usercore)
class activity_panel(admin.ModelAdmin):

    list_display=["username","gender"] #paneli özelleştiren
    list_display_links=["username"]  #basmalı yapan
    search_fields=["username","id"] #arama çubuğu oluşturan
    list_filter= ["username","id"] #sağda panel oluşturan
    
    class Meta:
        model=usercore