from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import os
import math

def replace_inf_with_string(obj):
    if isinstance(obj, dict):
        return {k: replace_inf_with_string(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_inf_with_string(v) for v in obj]
    elif isinstance(obj, float):
        if math.isinf(obj):
            return "Infinity" if obj > 0 else "-Infinity"
        elif math.isnan(obj):
            return "NaN"
    return obj

class SurvivalAnalysisView(APIView):
    def get(self, request):
        try:
            # Get the directory of the current file (views.py)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Construct the path to the JSON file
            json_file_path = os.path.join(current_dir, 'utils', 'survival_analysis_all_tickers_multi_threshold_lomax.json')
            
            # Read the JSON file
            with open(json_file_path, 'r') as file:
                survival_data = json.load(file)
            
            # Replace infinite values with strings
            survival_data = replace_inf_with_string(survival_data)
            
            # Get query parameters
            ticker = request.query_params.get('ticker')
            
            if ticker:
                # If a specific ticker is requested, return data for that ticker only
                if ticker in survival_data:
                    return Response(survival_data[ticker])
                else:
                    return Response({"error": f"Ticker {ticker} not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                # If no specific ticker is requested, return all data
                return Response(survival_data)

        except FileNotFoundError:
            return Response({"error": "Survival analysis data not found"}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)