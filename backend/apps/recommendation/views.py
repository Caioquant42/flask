
from .models import *

import json
import os
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from django.http import JsonResponse
from .utils.b3_utils import *

class BRStockRecommendationViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            # Construct the full path to the JSON file
            json_file_path = os.path.join(settings.BASE_DIR, 'apps', 'recommendation', 'utils', 'all_BR_recommendations.json')
            
            # Read the JSON file
            with open(json_file_path, 'r') as file:
                data = json.load(file)
            
            # Return the data as a response
            return Response(data)
        except FileNotFoundError:
            return Response({"error": "Data file not found"}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            # Construct the full path to the JSON file
            json_file_path = os.path.join(settings.BASE_DIR, 'apps', 'recommendation', 'utils', 'all_BR_recommendations.json')
            
            # Read the JSON file
            with open(json_file_path, 'r') as file:
                data = json.load(file)
            
            # Check if the requested ticker exists in the data
            if pk in data:
                return Response(data[pk])
            else:
                return Response({"error": "Ticker not found"}, status=status.HTTP_404_NOT_FOUND)
        except FileNotFoundError:
            return Response({"error": "Data file not found"}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NASDAQRecommendationViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            # Construct the full path to the JSON file
            json_file_path = os.path.join(settings.BASE_DIR, 'apps', 'recommendation', 'utils', 'all_USA_NASDAQ.json')
            
            # Read the JSON file
            with open(json_file_path, 'r') as file:
                data = json.load(file)
            
            # Return the data as a response
            return Response(data)
        except FileNotFoundError:
            return Response({"error": "Data file not found"}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            # Construct the full path to the JSON file
            json_file_path = os.path.join(settings.BASE_DIR, 'apps', 'recommendation', 'utils', 'all_USA_NASDAQ.json')
            
            # Read the JSON file
            with open(json_file_path, 'r') as file:
                data = json.load(file)
            
            # Check if the requested ticker exists in the data
            if pk in data:
                return Response(data[pk])
            else:
                return Response({"error": "Ticker not found"}, status=status.HTTP_404_NOT_FOUND)
        except FileNotFoundError:
            return Response({"error": "Data file not found"}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NYSERecommendationViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            # Construct the full path to the JSON file
            json_file_path = os.path.join(settings.BASE_DIR, 'apps', 'recommendation', 'utils', 'all_USA_NYSE.json')
            
            # Read the JSON file
            with open(json_file_path, 'r') as file:
                data = json.load(file)
            
            # Return the data as a response
            return Response(data)
        except FileNotFoundError:
            return Response({"error": "Data file not found"}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            # Construct the full path to the JSON file
            json_file_path = os.path.join(settings.BASE_DIR, 'apps', 'recommendation', 'utils', 'all_USA_NYSE.json')
            
            # Read the JSON file
            with open(json_file_path, 'r') as file:
                data = json.load(file)
            
            # Check if the requested ticker exists in the data
            if pk in data:
                return Response(data[pk])
            else:
                return Response({"error": "Ticker not found"}, status=status.HTTP_404_NOT_FOUND)
        except FileNotFoundError:
            return Response({"error": "Data file not found"}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

###############BR######################################################################################
def load_json_data():
    json_file_path = os.path.join(settings.BASE_DIR, 'apps', 'recommendation', 'utils', 'all_BR_recommendations.json')
    try:
        with open(json_file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None

def strong_buy_analysis(request):
    if request.method == 'GET':
        all_data = load_json_data()
        if all_data is None:
            return JsonResponse({'error': 'Unable to load data'}, status=500)
        
        print("Total number of stocks:", len(all_data))
        
        strong_buy_data = {
            ticker: stock_data
            for ticker, stock_data in all_data.items()
            if stock_data.get('recommendationKey') == 'strong_buy'
        }
        
        print("Number of strong buy stocks:", len(strong_buy_data))
        if len(strong_buy_data) > 0:
            print("Sample strong buy stock:", next(iter(strong_buy_data.items())))
        
        result = analyze_b3_data(strong_buy_data)
        return JsonResponse({'data': result})
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=400)

def buy_analysis(request):
    if request.method == 'GET':
        all_data = load_json_data()
        if all_data is None:
            return JsonResponse({'error': 'Unable to load data'}, status=500)
        
        buy_data = {
            ticker: stock_data
            for ticker, stock_data in all_data.items()
            if stock_data.get('recommendationKey') == 'buy'
        }
        
        result = analyze_b3_buy_data(buy_data)
        return JsonResponse({'data': result})
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=400)

######################NASDAQ#############################################
def nasdaq_load_json_data():
    json_file_path = os.path.join(settings.BASE_DIR, 'apps', 'recommendation', 'utils', 'all_USA_NASDAQ.json')
    try:
        with open(json_file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None

def nasdaq_strong_buy_analysis(request):
    if request.method == 'GET':
        all_data = nasdaq_load_json_data()
        if all_data is None:
            return JsonResponse({'error': 'Unable to load data'}, status=500)
        
        print("Total number of stocks:", len(all_data))
        
        strong_buy_data = {
            ticker: stock_data
            for ticker, stock_data in all_data.items()
            if stock_data.get('recommendationKey') == 'strong_buy'
        }
        
        print("Number of strong buy stocks:", len(strong_buy_data))
        if len(strong_buy_data) > 0:
            print("Sample strong buy stock:", next(iter(strong_buy_data.items())))
        
        result = analyze_b3_data(strong_buy_data)
        return JsonResponse({'data': result})
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=400)

def nasdaq_buy_analysis(request):
    if request.method == 'GET':
        all_data = nasdaq_load_json_data()
        if all_data is None:
            return JsonResponse({'error': 'Unable to load data'}, status=500)
        
        buy_data = {
            ticker: stock_data
            for ticker, stock_data in all_data.items()
            if stock_data.get('recommendationKey') == 'buy'
        }
        
        result = analyze_b3_buy_data(buy_data)
        return JsonResponse({'data': result})
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=400)
######################NYSE###############################################
def nyse_load_json_data():
    json_file_path = os.path.join(settings.BASE_DIR, 'apps', 'recommendation', 'utils', 'all_USA_NYSE.json')
    try:
        with open(json_file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None

def nyse_strong_buy_analysis(request):
    if request.method == 'GET':
        all_data = nyse_load_json_data()
        if all_data is None:
            return JsonResponse({'error': 'Unable to load data'}, status=500)
        
        print("Total number of stocks:", len(all_data))
        
        strong_buy_data = {
            ticker: stock_data
            for ticker, stock_data in all_data.items()
            if stock_data.get('recommendationKey') == 'strong_buy'
        }
        
        print("Number of strong buy stocks:", len(strong_buy_data))
        if len(strong_buy_data) > 0:
            print("Sample strong buy stock:", next(iter(strong_buy_data.items())))
        
        result = analyze_b3_data(strong_buy_data)
        return JsonResponse({'data': result})
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=400)

def nyse_buy_analysis(request):
    if request.method == 'GET':
        all_data = nyse_load_json_data()
        if all_data is None:
            return JsonResponse({'error': 'Unable to load data'}, status=500)
        
        buy_data = {
            ticker: stock_data
            for ticker, stock_data in all_data.items()
            if stock_data.get('recommendationKey') == 'buy'
        }
        
        result = analyze_b3_buy_data(buy_data)
        return JsonResponse({'data': result})
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=400)