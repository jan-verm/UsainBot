# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from maps.models import Map
from maps.serializers import MapSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from route import Route, generate_map_urls


class MapList(APIView):
    """
    get a map
    """
    def get(self, request, longtitude, lat, km, monumentbool, nr_of_mutations, format=None):
        location = [longtitude, lat]
        url_item = generate_map_urls(location, km, monumentbool, nr_of_mutations)
        map_item = Map(url = url_item)
        map_item.save()
        serializer = MapSerializer(map_item, many=False)
        return Response(serializer.data)

  