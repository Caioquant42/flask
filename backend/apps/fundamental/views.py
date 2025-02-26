from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import os
from pathlib import Path
from .utils.agenda_dividendos import fetch_and_save_dividend_data
import logging
import unidecode

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["GET"])
def get_dividend_agenda(request):
    # Get the path to the utils directory
    current_dir = Path(__file__).resolve().parent
    utils_dir = current_dir / 'utils'
    logger.info(f"Searching for dividend agenda files in: {utils_dir}")
    
    json_files = [f for f in os.listdir(utils_dir) if f.startswith('dividend_agenda_') and f.endswith('.json')]
    logger.info(f"Found {len(json_files)} dividend agenda files")
    
    if not json_files:
        logger.info("No existing files found. Attempting to fetch new data.")
        try:
            filename = fetch_and_save_dividend_data()
            json_files = [filename]
            logger.info(f"Successfully fetched and saved new data: {filename}")
        except Exception as e:
            logger.error(f"Failed to fetch dividend agenda data: {str(e)}")
            return JsonResponse({"error": f"Failed to fetch dividend agenda data: {str(e)}"}, status=500)
    
    if not json_files:
        logger.error("No dividend agenda data available even after attempting to fetch")
        return JsonResponse({"error": "No dividend agenda data available even after attempting to fetch"}, status=404)
    
    latest_file = max(json_files)
    file_path = utils_dir / latest_file
    logger.info(f"Attempting to read data from: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Format the data to be human-readable
        formatted_data = []
        for item in data:
            formatted_item = {unidecode.unidecode(k): v for k, v in item.items()}
            formatted_data.append(formatted_item)
        
        logger.info("Successfully read and formatted dividend agenda data")
        return JsonResponse(formatted_data, safe=False)
    except Exception as e:
        logger.error(f"Error reading dividend agenda data: {str(e)}")
        return JsonResponse({"error": f"Error reading dividend agenda data: {str(e)}"}, status=500)



from django.conf import settings

def statements_view(request):
    # Define the path to the JSON file
    file_path = os.path.join(settings.BASE_DIR, 'apps', 'fundamental', 'utils', 'statements_all.json')
    
    # Check if the file exists before attempting to open it
    if not os.path.exists(file_path):
        return JsonResponse({'error': 'Data file not found'}, status=404)
    
    # Open and read the JSON data
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': 'Error reading data', 'details': str(e)}, status=500)

def dividend_yield_view(request):
    # Define the path to the JSON file
    file_path = os.path.join(settings.BASE_DIR, 'apps', 'fundamental', 'utils', 'all_historical_dy.json')
    
    # Check if the file exists before attempting to open it
    if not os.path.exists(file_path):
        return JsonResponse({'error': 'Data file not found'}, status=404)
    
    # Open and read the JSON data
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': 'Error reading data', 'details': str(e)}, status=500)