from django.urls import path

from .views import query_emotion_model, query_sentiment_model

urlpatterns = [
  path("api/query_emotion_model/", query_emotion_model, name="query_emotion_model"),
  path("api/query_sentiment_model/", query_sentiment_model, name="query_sentiment_model"),
]