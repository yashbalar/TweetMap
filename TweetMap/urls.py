from django.conf.urls import url,include
from django.contrib import admin

from rest_framework.urlpatterns import format_suffix_patterns
from Tweets import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^tweets/', views.TweetList.as_view()),
    url(r'^', include('Map.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)