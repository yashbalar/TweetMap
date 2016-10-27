from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from .models import Tweet
from .serializer import TweetSerializer

import sys
import jsonpickle
import os
import tweepy
import json


# Lists all tweets
# tweets/
class TweetList(APIView):
    def get(self, request):
        # Replace the API_KEY and API_SECRET with your application's key and secret.
        auth = tweepy.AppAuthHandler('DBJmB2c1oF5OxaEebqLv77Q4d', 'Zplv8oMt6r2Jjl6O9HbiatId1FKVfRJrfM1GbyBhWdngWFzagx')

        api = tweepy.API(auth, wait_on_rate_limit=True,
                         wait_on_rate_limit_notify=True)

        searchQuery = self.request.query_params.get('search', None)
        if searchQuery:

            print(searchQuery)
            maxTweets = 500  # Some arbitrary large number
            tweetsPerQry = 100  # this is the max the API permits

            # If results from a specific ID onwards are reqd, set since_id to that ID.
            # else default to no lower limit, go as far back as API allows
            sinceId = None

            # If results only below a specific ID are, set max_id to that ID.
            # else default to no upper limit, start from the most recent tweet matching the search query.
            max_id = -1

            tweetCount = 0
            print("Downloading max {0} tweets".format(maxTweets))

            tweetCollection = []
            while tweetCount < maxTweets:
                try:
                    if (max_id <= 0):
                        if (not sinceId):
                            new_tweets = api.search(q=searchQuery, geocode="37.781157,-122.398720,3959mi",count=tweetsPerQry)
                        else:
                            new_tweets = api.search(q=searchQuery, geocode="37.781157,-122.398720,3959mi",count=tweetsPerQry,
                                                    since_id=sinceId)
                    else:
                        if (not sinceId):
                            new_tweets = api.search(q=searchQuery, geocode="37.781157,-122.398720,3959mi", count=tweetsPerQry,
                                                    max_id=str(max_id - 1))
                        else:
                            new_tweets = api.search(q=searchQuery, geocode="37.781157,-122.398720,3959mi", count=tweetsPerQry,
                                                    max_id=str(max_id - 1),
                                                    since_id=sinceId)
                    if not new_tweets:
                        print("No more tweets found")
                        break

                    for tweet in new_tweets:
                        json_line = jsonpickle.encode(tweet._json, unpicklable=False) + '\n'
                        tweet = json.loads(json_line)

                        if tweet['coordinates']:
                            tempTweet = Tweet.create(tweet['coordinates']['coordinates'][0],tweet['coordinates']['coordinates'][1],tweet['text'])

                            tweetCollection.append(tempTweet)
                    tweetCount += len(new_tweets)
                    max_id = new_tweets[-1].id
                except tweepy.TweepError as e:
                    # Just exit if any error
                    print("some error : " + str(e))
                    break

            tweets = Tweet.objects.all()
            
            tweets = tweets.filter(text__contains=searchQuery)
            serializer1 = TweetSerializer(tweets, many=True)
            serializer = TweetSerializer(tweetCollection, many=True)
            return Response(serializer.data + serializer1.data)
        else:
            tweets = Tweet.objects.all()
            serializer = TweetSerializer(tweets, many=True)
            return Response(serializer.data)

    def post(self):
        tweets = Tweet.objects.all()
        serializer = TweetSerializer(tweets, many=True)
        return Response(serializer.data)

    # def get(self,request):
    #     f = open("C:/Users/Yash/Desktop/tweetcollection.txt")
    #     for line in f:
    #         try:
    #             line = line.strip('\n')
    #             line = line.split('|')
    #             text = line[1]
    #             latitude = float(line[3])
    #             longitude = float(line[2])
    #             new_tweet = Tweet(text=text, lat=latitude, lon=longitude)
    #             new_tweet.save()
    #         except:
    #             continue
    #     return HTTPResponse("hello")