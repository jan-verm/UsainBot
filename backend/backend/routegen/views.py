# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User, Group
from .models import Map
from rest_framework import viewsets
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .serializers import UserSerializer, GroupSerializer, MapSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .route import Route
from .models import Map

import geog
import networkx as nx
import osmgraph
import random
import itertools
import geojsonio
import json


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

@api_view(['GET'])
def map(request, km, monumentbool, location):
    """
    List all code maps
    """
    if request.method == 'GET':
        urls = Route.generate_map_urls(location, km, monumentbool, 20)
        map_new = Map(url = urls)
        map_new.save()
        serializer = MapSerializer(map_new, many=False)
        return Response(serializer.data)
