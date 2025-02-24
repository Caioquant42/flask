# recomendations/management/commands/refresh_usa_recommendations.py
from django.core.management.base import BaseCommand
from apps.recomendations.models import USAStockRecommendation
from apps.utils.dict import USA_TICKERS_DICT
from apps.recomendations.utils.recomendations_utils import get_analyst_information
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Refreshes the USAStockRecommendation database with data from the API.'

    def handle(self, *args, **options):
        self.stdout.write("Refreshing USAStockRecommendation data...")
        try:
            # Flatten the USA_TICKERS_DICT to get all tickers
            all_tickers = [ticker for exchange_tickers in USA_TICKERS_DICT.values() for ticker in exchange_tickers]

            if not all_tickers:
                self.stdout.write(self.style.WARNING("No tickers found in USA_TICKERS_DICT."))
                return

            analyst_info_df = get_analyst_information(all_tickers, world=True)
            if analyst_info_df is not None:
                USAStockRecommendation.objects.all().delete()  # Clear existing data
                USAStockRecommendation.objects.bulk_create([
                    USAStockRecommendation(
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
                        update_id=1
                    ) for row in analyst_info_df.to_dict('records')
                ])
                self.stdout.write(self.style.SUCCESS('USAStockRecommendation data refreshed successfully!'))
            else:
                self.stdout.write(self.style.WARNING('No data found for the tickers.'))
        except Exception as e:
            logger.exception(f"An error occurred while refreshing data: {e}")
            self.stdout.write(self.style.ERROR(f'Error refreshing USAStockRecommendation data: {e}'))

# future updates, store the information gathered after each sucefful request to save the data in case of API denial or any other motive