import subprocess
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import sys


import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def optimize_portfolio_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            stocks = data.get('stocks')
            period = data.get('period')
            logger.info(f"Processing request for stocks: {stocks}, period: {period}")

            current_dir = os.path.dirname(os.path.abspath(__file__))
            opt_script_path = os.path.join(current_dir, 'utils', 'opt.py')

            # Use the same Python interpreter that's running Django
            python_executable = sys.executable

            command = [
                python_executable,
                opt_script_path,
                '--stocks', ','.join(stocks),
                '--period', str(period)
            ]

            logger.debug(f"Executing command: {' '.join(command)}")
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            logger.debug(f"Script output: {result.stdout}")

            optimization_results = json.loads(result.stdout)
            logger.info("Successfully processed optimization request")
            return JsonResponse(optimization_results)

        except Exception as e:
            logger.error(f"Error in optimize_portfolio_view: {str(e)}")
            logger.exception("Full traceback:")
            return JsonResponse({'error': str(e)}, status=500)

    logger.warning("Received non-POST request")
    return JsonResponse({'error': 'Invalid request method'}, status=400)