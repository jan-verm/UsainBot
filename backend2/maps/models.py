from django.db import models



class Map(models.Model):
    url = models.CharField(max_length=200, default='')

    class Meta:
        ordering = ('url',)