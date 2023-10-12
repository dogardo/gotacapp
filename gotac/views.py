from django.shortcuts import render, HttpResponse
from account.models import *
from activities.models import *
import random

def index(request):

    allhashtags = hashtags.objects.all()

    allplaces = places.objects.all()

    allcommunities = communities.objects.all()

    alllist = list(allhashtags) + list(allplaces) + list(allcommunities)

    random.shuffle(alllist)

    first_list = alllist[:1]
    second_list = alllist[1:4]
    thirth_list = alllist[4:8]

    values= {
        "list1":first_list,
        "list2":second_list,
        "list3":thirth_list,
    }

    return render(request,"index.html",values)