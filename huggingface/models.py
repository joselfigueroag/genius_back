from django.db import models

# Create your models here.


class Comment(models.Model):
  class EmotionLabel(models.TextChoices):
    JOY = "joy"
    FEAR = "fear"
    SADNESS = "sadness"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    ANGER = "anger"
    OTHERS = "others"
    ERROR = "error"
  
  class SentimentLabel(models.TextChoices):
    POS = "POS"
    NEG = "NEG"
    NEU = "NEU"
    ERROR = "ERROR"

  text = models.TextField(verbose_name="texto")
  emotion_label = models.CharField(max_length=10, verbose_name="etiqueta de emocion", choices=EmotionLabel.choices)
  sentiment_label = models.CharField(max_length=5, verbose_name="etiqueta sentimiento", choices=SentimentLabel.choices)
