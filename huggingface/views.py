import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import pandas as pd
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .process_data import process_data

# Create your views here.


@api_view(('POST',))
@permission_classes([IsAuthenticated])
@csrf_exempt
def query_emotion_model(request):
  file = request.FILES.get("file")
  df = pd.read_csv(file, usecols=['text'])
  df['emotion_label'] = df["text"].apply(process_data.emotion_model)
  count_emotions = df['emotion_label'].value_counts()

  data_json = json.loads(df.to_json(orient='records'))
  count_emotions_json = json.loads(count_emotions.to_json())

  return Response({"data": data_json, "count_labels": count_emotions_json})


@api_view(('POST',))
@permission_classes([IsAuthenticated])
@csrf_exempt
def query_sentiment_model(request):
  file = request.FILES.get("file")
  df = pd.read_csv(file, usecols=['text'])
  df['sentiment_label'] = df["text"].apply(process_data.sentiment_model)
  count_sentiments = df['sentiment_label'].value_counts()

  data_json = json.loads(df.to_json(orient='records'))
  count_sentiments_json = json.loads(count_sentiments.to_json())

  return Response({"data": data_json, "count_labels": count_sentiments_json})
