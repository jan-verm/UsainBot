# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Map(models.Model):
    url = models.URLField(max_length=200)

    class Meta:
        ordering = ('created',)