from django.shortcuts import render
from django.http import JsonResponse
from .db_connect import collection, collectionCart
from django.http import HttpResponse
from prefixspan import PrefixSpan
from django.core.serializers.json import DjangoJSONEncoder
from bson import ObjectId
def index(request):
    return HttpResponse("Welcome to my Django API 222")