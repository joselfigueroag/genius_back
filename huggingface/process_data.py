import requests

EMOTION_ENDPOINT = "https://api-inference.huggingface.co/models/finiteautomata/beto-emotion-analysis"
SENTIMENT_ENDPOINT = "https://api-inference.huggingface.co/models/finiteautomata/beto-sentiment-analysis"


class ProcessData:
  def __init__(self, *args, **kwargs):
    self.httpClient = requests.Session()
    self.httpClient.headers.update(
      {"Authorization": "Bearer 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"}
    )

  def emotion_model(self, data):
    response = self.httpClient.request("POST", EMOTION_ENDPOINT, json=data)
    label = response.json()[0][0]["label"]
    return label

  def sentiment_model(self, data):
    response = self.httpClient.request("POST", SENTIMENT_ENDPOINT, json=data)
    label = response.json()[0][0]["label"]
    return label

process_data = ProcessData()
