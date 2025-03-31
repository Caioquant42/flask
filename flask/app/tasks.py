import subprocess
from app import celery

@celery.task
def run_fetch_surface():
    try:
        result = subprocess.run([
            '/var/www/fullstack/backenv/bin/python',
            '/var/www/fullstack/flask/app/utils/fetch_surface.py'
        ], capture_output=True, text=True, check=True)
        print(result.stdout)
        return "Fetch surface script executed successfully"
    except subprocess.CalledProcessError as e:
        print(f"Error executing fetch surface script: {e}")
        print(f"Script output: {e.output}")
        return f"Error executing fetch surface script: {e}"

@celery.task
def run_volatility_analysis():
    try:
        result = subprocess.run([
            '/var/www/fullstack/backenv/bin/python',
            '/var/www/fullstack/flask/app/utils/volatility_analysis.py'
        ], capture_output=True, text=True, check=True)
        print(result.stdout)
        return "Volatility Analysis script executed successfully"
    except subprocess.CalledProcessError as e:
        print(f"Error executing Volatility Analysis script: {e}")
        print(f"Script output: {e.output}")
        return f"Error executing Volatility Analysis script: {e}"