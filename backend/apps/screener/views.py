import json
import os
from django.http import JsonResponse
from django.conf import settings

def rsi_analysis(request):
    if request.method == 'GET':
        try:
            # Path to the JSON file
            json_file_path = os.path.join(settings.BASE_DIR, 'apps', 'screener', 'utils', 'ibov_overbought_oversold_rsi_results.json')

            # Read the JSON file
            with open(json_file_path, 'r') as file:
                data = json.load(file)

            # Prepare data for response
            response_data = {
                "15m": {
                    "overbought": data["stockdata_15m"]["overbought"],
                    "oversold": data["stockdata_15m"]["oversold"]
                },
                "60m": {
                    "overbought": data["stockdata_60m"]["overbought"],
                    "oversold": data["stockdata_60m"]["oversold"]
                },
                "1d": {
                    "overbought": data["stockdata_1d"]["overbought"],
                    "oversold": data["stockdata_1d"]["oversold"]
                },
                "1w": {
                    "overbought": data["stockdata_1wk"]["overbought"],
                    "oversold": data["stockdata_1wk"]["oversold"]
                }
            }

            return JsonResponse(response_data)

        except FileNotFoundError:
            return JsonResponse({'error': 'RSI analysis data not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=500)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)