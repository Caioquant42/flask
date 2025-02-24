from django.db import models

class BRStockRecommendation(models.Model):
    ticker = models.CharField(max_length=10)  
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    recommendation_key = models.CharField(max_length=20, null=True, blank=True)
    number_of_analyst_opinions = models.IntegerField(null=True, blank=True)
    target_median_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    target_mean_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    target_low_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    target_high_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    distance_to_median = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    distance_to_low = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    distance_to_high = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)  # Automatically updates on save
    update_id = models.IntegerField(default=1)  

    class Meta:
        unique_together = ('ticker', 'update_id')  # Ensure the combination of ticker and update_id is unique

    def __str__(self):
        return self.ticker

class USAStockRecommendation(models.Model):
    ticker = models.CharField(max_length=10)  
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    recommendation_key = models.CharField(max_length=20, null=True, blank=True)
    number_of_analyst_opinions = models.IntegerField(null=True, blank=True)
    target_median_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    target_mean_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    target_low_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    target_high_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    distance_to_median = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    distance_to_low = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    distance_to_high = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)  # Automatically updates on save
    update_id = models.IntegerField(default=1)  

    class Meta:
        unique_together = ('ticker', 'update_id')  # Ensure the combination of ticker and update_id is unique

    def __str__(self):
        return self.ticker