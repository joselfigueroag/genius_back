import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import pandas as pd
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


from .process_data import process_data

# Create your views here.


@api_view(('POST',))
@permission_classes([IsAuthenticated])
@csrf_exempt
def query_emotion_model_view(request):
  file = request.FILES.get("file")

  if not file:
    return Response({"msg": "Debe cargar un archivo CSV"}, status=status.HTTP_400_BAD_REQUEST)

  df = pd.read_csv(file, usecols=['text'])
  df['label'] = df["text"].apply(process_data.emotion_model)
  count_emotions = df['label'].value_counts()

  data_json = json.loads(df.to_json(orient='records'))
  count_emotions_json = json.loads(count_emotions.to_json())

  return Response({"data": data_json, "count_labels": count_emotions_json, "motive": "emotions"})


@api_view(('POST',))
@permission_classes([IsAuthenticated])
@csrf_exempt
def query_sentiment_model_view(request):
  file = request.FILES.get("file")

  if not file:
    return Response({"msg": "Debe cargar un archivo CSV"}, status=status.HTTP_400_BAD_REQUEST)

  df = pd.read_csv(file, usecols=['text'])
  df['label'] = df["text"].apply(process_data.sentiment_model)
  count_sentiments = df['label'].value_counts()

  data_json = json.loads(df.to_json(orient='records'))
  count_sentiments_json = json.loads(count_sentiments.to_json())

  return Response({"data": data_json, "count_labels": count_sentiments_json, "motive": "sentiments"})
