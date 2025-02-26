from django.core.management.base import BaseCommand
from apps.screener.utils.screener_utils import screener_rsi
from apps.screener.models import RSIAnalysis

class Command(BaseCommand):
    help = 'Calculate RSI and store the results in the database'

    def handle(self, *args, **kwargs):
        # Clear existing data in the database
        RSIAnalysis.objects.all().delete()

        # Analyze RSI for both tables
        overbought_15m, oversold_15m = screener_rsi("stockdata_15m", "15m")
        overbought_60m, oversold_60m = screener_rsi("stockdata_60m", "60m")
        overbought_1d, oversold_1d = screener_rsi("stockdata_1d", "1d")
        overbought_1w, oversold_1w = screener_rsi("stockdata_1w", "1w")


        # Save results to the database
        for df, interval, condition in [
            (overbought_60m, "60m", "overbought"),
            (oversold_60m, "60m", "oversold"),
            (overbought_1d, "1d", "overbought"),
            (oversold_1d, "1d", "oversold"),
            (overbought_15m, "15m", "overbought"),
            (oversold_15m, "15m", "oversold"),
            (overbought_1w, "1w", "overbought"),
            (oversold_1w, "1w", "oversold")
        ]:
            for _, row in df.iterrows():
                RSIAnalysis.objects.create(
                    datetime=row['Datetime'],
                    symbol=row['Symbol'],
                    close=row['Close'],
                    rsi=row['RSI'],
                    interval=interval,
                    condition=condition
                )

        self.stdout.write(self.style.SUCCESS('Successfully calculated and saved RSI data'))
