import json
from django.http import JsonResponse
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from datetime import datetime

class FluxoJsonView(APIView):
    def get(self, request):
        try:
            json_file_path = os.path.join(settings.BASE_DIR, 'apps', 'endpoint', 'utils', 'fluxo.json')
            
            print(f"File path: {json_file_path}")
            
            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                print("JSON data loaded successfully")
                print(f"Number of records: {len(data)}")
                print(f"First record: {data[0]}")
                print(f"Last record: {data[-1]}")

            # Sort the data by date in descending order
            sorted_data = sorted(data, key=lambda x: datetime.strptime(x['Data'], '%d/%m/%Y'), reverse=True)

            # Ensure all fields are present in each record
            expected_fields = ["Data", "Estrangeiro", "Institucional", "Pessoa física", "Inst. Financeira", "Outros", "Todos"]
            for record in sorted_data:
                for field in expected_fields:
                    if field not in record:
                        record[field] = "N/A"

            return Response(sorted_data)
        except Exception as e:
            print(f"Error: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def stocks_json(request):
    try:
        # Correcting the file path according to your directory structure indicating `backend/apps/endpoint/utils`
        json_file_path = os.path.join(
            os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')),
            'apps', 'endpoint', 'utils', 'IBOV_stocks.json'
        )

        print(f"File path: {json_file_path}")  # Debugging line to verify correct path
    
        # Attempt to open and read the JSON file
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            print("JSON data loaded successfully")  # Debugging confirmation

        return JsonResponse(data, safe=False)
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'error': str(e)}, status=500)

class SurfaceView(APIView):
    def get(self, request):
        try:
            # Construct the full path to the JSON file
            json_file_path = os.path.join(settings.BASE_DIR, 'apps', 'endpoint', 'utils', 'all_tickers_last_time_data.json')
            
            # Read the JSON file
            with open(json_file_path, 'r') as file:
                surface_data = json.load(file)
            
            # You can add pagination here if needed
            
            return Response(surface_data)
        except FileNotFoundError:
            return Response({"error": "Surface data analysis results not found"}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class COLLAR14View(APIView):
    def get(self, request):
        try:
            # Construct the full path to the JSON file
            json_file_path = os.path.join(settings.BASE_DIR, 'apps', 'endpoint', 'utils', 'intrinsic_options_less_than_14_days.json')
            
            # Read the JSON file
            with open(json_file_path, 'r') as file:
                surface_data = json.load(file)
            
            # You can add pagination here if needed
            
            return Response(surface_data)
        except FileNotFoundError:
            return Response({"error": "Collar data analysis results not found"}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class COLLAR30View(APIView):
    def get(self, request):
        try:
            # Construct the full path to the JSON file
            json_file_path = os.path.join(settings.BASE_DIR, 'apps', 'endpoint', 'utils', 'intrinsic_options_between_15_and_30_days.json')
            
            # Read the JSON file
            with open(json_file_path, 'r') as file:
                surface_data = json.load(file)
            
            # You can add pagination here if needed
            
            return Response(surface_data)
        except FileNotFoundError:
            return Response({"error": "Collar data analysis results not found"}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class COLLAR60View(APIView):
    def get(self, request):
        try:
            # Construct the full path to the JSON file
            json_file_path = os.path.join(settings.BASE_DIR, 'apps', 'endpoint', 'utils', 'intrinsic_options_between_30_and_60_days.json')
            
            # Read the JSON file
            with open(json_file_path, 'r') as file:
                surface_data = json.load(file)
            
            # You can add pagination here if needed
            
            return Response(surface_data)
        except FileNotFoundError:
            return Response({"error": "Collar data analysis results not found"}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class COLLARABOVE60View(APIView):
    def get(self, request):
        try:
            # Construct the full path to the JSON file
            json_file_path = os.path.join(settings.BASE_DIR, 'apps', 'endpoint', 'utils', 'intrinsic_options_more_than_60_days.json')
            
            # Read the JSON file
            with open(json_file_path, 'r') as file:
                surface_data = json.load(file)
            
            # You can add pagination here if needed
            
            return Response(surface_data)
        except FileNotFoundError:
            return Response({"error": "Collar data analysis results not found"}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OTMCOLLAR14View(APIView):
    def get(self, request):
        try:
            # Construct the full path to the JSON file
            json_file_path = os.path.join(settings.BASE_DIR, 'apps', 'endpoint', 'utils', 'otm_options_less_than_14_days.json')
            
            # Read the JSON file
            with open(json_file_path, 'r') as file:
                surface_data = json.load(file)
            
            # You can add pagination here if needed
            
            return Response(surface_data)
        except FileNotFoundError:
            return Response({"error": "Collar data analysis results not found"}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OTMCOLLAR30View(APIView):
    def get(self, request):
        try:
            # Construct the full path to the JSON file
            json_file_path = os.path.join(settings.BASE_DIR, 'apps', 'endpoint', 'utils', 'otm_options_between_15_and_30_days.json')
            
            # Read the JSON file
            with open(json_file_path, 'r') as file:
                surface_data = json.load(file)
            
            # You can add pagination here if needed
            
            return Response(surface_data)
        except FileNotFoundError:
            return Response({"error": "Collar data analysis results not found"}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OTMCOLLAR60View(APIView):
    def get(self, request):
        try:
            # Construct the full path to the JSON file
            json_file_path = os.path.join(settings.BASE_DIR, 'apps', 'endpoint', 'utils', 'otm_options_between_30_and_60_days.json')
            
            # Read the JSON file
            with open(json_file_path, 'r') as file:
                surface_data = json.load(file)
            
            # You can add pagination here if needed
            
            return Response(surface_data)
        except FileNotFoundError:
            return Response({"error": "Collar data analysis results not found"}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OTMCOLLARABOVE60View(APIView):
    def get(self, request):
        try:
            # Construct the full path to the JSON file
            json_file_path = os.path.join(settings.BASE_DIR, 'apps', 'endpoint', 'utils', 'otm_options_more_than_60_days.json')
            
            # Read the JSON file
            with open(json_file_path, 'r') as file:
                surface_data = json.load(file)
            
            # You can add pagination here if needed
            
            return Response(surface_data)
        except FileNotFoundError:
            return Response({"error": "Collar data analysis results not found"}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CointegrationView(APIView):
    def get(self, request):
        try:
            # Construct the full path to the JSON file
            json_file_path = os.path.join(settings.BASE_DIR, 'apps', 'endpoint', 'utils', 'combined_cointegration_results.json')
            
            # Read the JSON file
            with open(json_file_path, 'r') as file:
                surface_data = json.load(file)
            
            # You can add pagination here if needed
            
            return Response(surface_data)
        except FileNotFoundError:
            return Response({"error": "Cointegration data analysis results not found"}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CurrencyCointegrationView(APIView):
    def get(self, request):
        try:
            # Construct the full path to the JSON file
            json_file_path = os.path.join(settings.BASE_DIR, 'apps', 'endpoint', 'utils', 'combined_currency_cointegration_results.json')
            
            # Read the JSON file
            with open(json_file_path, 'r') as file:
                surface_data = json.load(file)
            
            # You can add pagination here if needed
            
            return Response(surface_data)
        except FileNotFoundError:
            return Response({"error": "Cointegration data analysis results not found"}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RRGView(APIView):
    def get(self, request):
        try:
            # Construct the full path to the JSON file
            json_file_path = os.path.join(settings.BASE_DIR, 'apps', 'endpoint', 'utils', 'rrg_data.json')
            
            # Read the JSON file
            with open(json_file_path, 'r') as file:
                surface_data = json.load(file)
            
            # You can add pagination here if needed
            
            return Response(surface_data)
        except FileNotFoundError:
            return Response({"error": "Cointegration data analysis results not found"}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RRGINDEXView(APIView):
    def get(self, request):
        try:
            # Construct the full path to the JSON file
            json_file_path = os.path.join(settings.BASE_DIR, 'apps', 'endpoint', 'utils', 'rrg_indices_data.json')
            
            # Read the JSON file
            with open(json_file_path, 'r') as file:
                surface_data = json.load(file)
            
            # You can add pagination here if needed
            
            return Response(surface_data)
        except FileNotFoundError:
            return Response({"error": "Cointegration data analysis results not found"}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class VolatilityAnalysisView(APIView):
    def get(self, request):
        try:
            # Construct the full path to the JSON file
            json_file_path = os.path.join(settings.BASE_DIR, 'apps', 'endpoint', 'utils', 'volatility_analysis_results.json')
            
            # Read the JSON file
            with open(json_file_path, 'r') as file:
                volatility_data = json.load(file)
            
            # You can add pagination here if needed
            
            return Response(volatility_data)
        except FileNotFoundError:
            return Response({"error": "Volatility analysis results not found"}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TopVolatilityStocksView(APIView):
    def get(self, request):
        try:
            # Construct the full path to the JSON file
            json_file_path = os.path.join(settings.BASE_DIR, 'apps', 'endpoint', 'utils', 'volatility_analysis_results.json')
            
            # Read the JSON file
            with open(json_file_path, 'r') as file:
                volatility_data = json.load(file)
            
            # Sort the data by iv_to_ewma_ratio_current in descending order
            sorted_data = sorted(volatility_data, key=lambda x: x['iv_to_ewma_ratio_current'], reverse=True)
            
            # Get the top 10 stocks
            top_10_stocks = sorted_data[:10]
            
            return Response(top_10_stocks)
        except FileNotFoundError:
            return Response({"error": "Volatility analysis results not found"}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)