# recomendations/management/commands/refresh_recommendations.py
from django.core.management.base import BaseCommand
from apps.recommendation.models import BRStockRecommendation
from apps.utils.dict import TICKERS_DICT
from apps.recommendation.utils.recomendations_utils import get_analyst_information
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Refreshes the BRStockRecommendation database with data from the API.'

    def handle(self, *args, **options):
        self.stdout.write("Refreshing BRStockRecommendation data...")
        try:
            # Access tickers directly from the 'TODOS' key
            BR_tickers = TICKERS_DICT.get('TODOS', []) 

            if not BR_tickers:
                self.stdout.write(self.style.WARNING("The 'TODOS' key not found in TICKERS_DICT or is empty."))
                return

            analyst_info_df = get_analyst_information(BR_tickers)
            if analyst_info_df is not None:
                BRStockRecommendation.objects.all().delete()  # Clear existing data
                BRStockRecommendation.objects.bulk_create([
                    BRStockRecommendation(
                        ticker=row['Ticker'],
                        current_price=Decimal(str(row.get('currentPrice', 0))),
                        recommendation_key=row.get('recommendationKey', 'N/A'),
                        number_of_analyst_opinions=row.get('numberOfAnalystOpinions', 0),
                        target_median_price=Decimal(str(row.get('targetMedianPrice', 0))),
                        target_mean_price=Decimal(str(row.get('targetMeanPrice', 0))),
                        target_low_price=Decimal(str(row.get('targetLowPrice', 0))),
                        target_high_price=Decimal(str(row.get('targetHighPrice', 0))),
                        distance_to_median=Decimal(str(row.get('% Distance to Median', 0))),
                        distance_to_low=Decimal(str(row.get('% Distance to Low', 0))),
                        distance_to_high=Decimal(str(row.get('% Distance to High', 0))),
                    ) for row in analyst_info_df.to_dict('records')
                ])
                self.stdout.write(self.style.SUCCESS('BRStockRecommendation data refreshed successfully!'))
            else:
                self.stdout.write(self.style.WARNING('No data found for the tickers.'))
        except Exception as e:
            logger.exception(f"An error occurred while refreshing data: {e}")
            self.stdout.write(self.style.ERROR(f'Error refreshing BRStockRecommendation data: {e}'))
