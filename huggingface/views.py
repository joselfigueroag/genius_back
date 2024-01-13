from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .process_data import process_data

# Create your views here.


@api_view(('POST',))
@csrf_exempt
def query_emotion_model(request):
  file = request.FILES.get("file")
  df = pd.read_csv(file, usecols=['text'])
  df['emotion_label'] = df["text"].apply(process_data.emotion_model)
  print(df)

  count_emotions = df['emotion_label'].value_counts()

  result_json = df.to_json(orient='records')

  return Response({"data": result_json, "labels": count_emotions})


@api_view(('POST',))
@csrf_exempt
def query_sentiment_model(request):
  file = request.FILES.get("file")
  df = pd.read_csv(file, usecols=['text'])
  labels = df["text"].apply(process_data.sentiment_model)
  count_sentiments = labels.value_counts()
  print(count_sentiments)
  return Response({"labels": labels})
