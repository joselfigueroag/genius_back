import requests
from decouple import config

from .models import Comment

EMOTION_ENDPOINT = "https://api-inference.huggingface.co/models/finiteautomata/beto-emotion-analysis"
SENTIMENT_ENDPOINT = "https://api-inference.huggingface.co/models/finiteautomata/beto-sentiment-analysis"


class ProcessData:
  def __init__(self, *args, **kwargs):
    self.httpClient = requests.Session()
    self.httpClient.headers.update(
      {"Authorization": f"Bearer {config('HUGGING_FACE_TOKEN')}"}
    )

  def emotion_model(self, data):
    comment, created = Comment.objects.get_or_create(
      text=data, defaults={"emotion_label": "error"}
    )

    if comment.emotion_label and comment.emotion_label != Comment.EmotionLabel.ERROR:
      print("Procesado por DB")
      return comment.emotion_label
    
    print("Procesado por API")
    response = self.httpClient.request("POST", EMOTION_ENDPOINT, json=data)
    if response.status_code == 200:
      label = response.json()[0][0]["label"]
    else:
      label = "error"
      print(response.content)
    
    comment.emotion_label = label
    comment.save()
    return label

  def sentiment_model(self, data):
    comment, created = Comment.objects.get_or_create(
      text=data, defaults={"sentiment_label": "ERROR"}
    )

    if comment.sentiment_label and comment.sentiment_label != Comment.SentimentLabel.ERROR:
      print("Procesado por DB")
      return comment.sentiment_label

    print("Procesado por API")
    response = self.httpClient.request("POST", SENTIMENT_ENDPOINT, json=data)
    if response.status_code == 200:
      label = response.json()[0][0]["label"]
    else:
      label = "ERROR"
      print(response.content)
    
    comment.sentiment_label = label
    comment.save()
    return label

process_data = ProcessData()
