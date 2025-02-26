from django.db import models

class RSIAnalysis(models.Model):
    datetime = models.DateTimeField()
    symbol = models.CharField(max_length=10)
    close = models.FloatField()
    rsi = models.FloatField()
    interval = models.CharField(max_length=5)  # '60m' or '1d'
    condition = models.CharField(max_length=10)  # 'overbought' or 'oversold'

    def __str__(self):
        return f"{self.symbol} - {self.rsi} ({self.condition})"