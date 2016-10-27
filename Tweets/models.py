from __future__ import unicode_literals

from django.db import models

class Tweet(models.Model):
    text = models.CharField(max_length=500, default="abc")
    lon = models.FloatField()
    lat = models.FloatField()

    @classmethod
    def create(cls, longitude, latitude, tweet_text):
        book = cls(text=tweet_text, lon=longitude,lat=latitude)
        # do something with the book
        return book

    def __str__(self):
        return self.text + str(self.lat)+" "+str(self.lon)


