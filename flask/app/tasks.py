import subprocess
from app import celery

@celery.task
def run_ibov_stocks():
    try:
        result = subprocess.run([
            '/var/www/backenv/bin/python',
            '/var/www/fullstack/flask/app/utils/ibov_stocks.py'
        ], capture_output=True, text=True, check=True)
        print(result.stdout)
        return "ibov_stocks Analysis script executed successfully"
    except subprocess.CalledProcessError as e:
        print(f"Error executing ibov_stocks Analysis script: {e}")
        print(f"Script output: {e.output}")
        return f"Error executing ibov_stocks Analysis script: {e}"

@celery.task
def run_fetch_br_recommendations():
    try:
        result = subprocess.run([
            '/var/www/backenv/bin/python',
            '/var/www/fullstack/flask/app/utils/fetch_br_recommendations.py'
        ], capture_output=True, text=True, check=True)
        print(result.stdout)
        return "BR recommendations Analysis script executed successfully"
    except subprocess.CalledProcessError as e:
        print(f"Error executing BR recommendations Analysis script: {e}")
        print(f"Script output: {e.output}")
        return f"Error executing BR recommendations Analysis script: {e}"

@celery.task
def run_fetch_nasdaq_recommendations():
    try:
        result = subprocess.run([
            '/var/www/backenv/bin/python',
            '/var/www/fullstack/flask/app/utils/fetch_nasdaq_recommendations.py'
        ], capture_output=True, text=True, check=True)
        print(result.stdout)
        return "Nasdaq recommendations Analysis script executed successfully"
    except subprocess.CalledProcessError as e:
        print(f"Error executing Nasdaq recommendations Analysis script: {e}")
        print(f"Script output: {e.output}")
        return f"Error executing Nasdaq recommendations Analysis script: {e}"

@celery.task
def run_fetch_nyse_recommendations():
    try:
        result = subprocess.run([
            '/var/www/backenv/bin/python',
            '/var/www/fullstack/flask/app/utils/fetch_nyse_recommendations.py'
        ], capture_output=True, text=True, check=True)
        print(result.stdout)
        return "Nyse recommendations Analysis script executed successfully"
    except subprocess.CalledProcessError as e:
        print(f"Error executing Nyse recommendations Analysis script: {e}")
        print(f"Script output: {e.output}")
        return f"Error executing Nyse recommendations Analysis script: {e}"

@celery.task
def run_fetch_agenda_dividendos():
    try:
        result = subprocess.run([
            '/var/www/backenv/bin/python',
            '/var/www/fullstack/flask/app/utils/agenda_dividendos.py'
        ], capture_output=True, text=True, check=True)
        print(result.stdout)
        return "Agenda Analysis script executed successfully"
    except subprocess.CalledProcessError as e:
        print(f"Error executing Agenda Analysis script: {e}")
        print(f"Script output: {e.output}")
        return f"Error executing Agenda Analysis script: {e}"

@celery.task
def run_statements():
    try:
        result = subprocess.run([
            '/var/www/backenv/bin/python',
            '/var/www/fullstack/flask/app/utils/statements.py'
        ], capture_output=True, text=True, check=True)
        print(result.stdout)
        return "statements Analysis script executed successfully"
    except subprocess.CalledProcessError as e:
        print(f"Error executing statements Analysis script: {e}")
        print(f"Script output: {e.output}")
        return f"Error executing statements Analysis script: {e}"

@celery.task
def run_ddm_historical_dy():
    try:
        result = subprocess.run([
            '/var/www/backenv/bin/python',
            '/var/www/fullstack/flask/app/utils/ddm_historical_dy.py'
        ], capture_output=True, text=True, check=True)
        print(result.stdout)
        return "ddm_historical_dy Analysis script executed successfully"
    except subprocess.CalledProcessError as e:
        print(f"Error executing ddm_historical_dy Analysis script: {e}")
        print(f"Script output: {e.output}")
        return f"Error executing ddm_historical_dy Analysis script: {e}"

@celery.task
def run_screener_yf():
    try:
        result = subprocess.run([
            '/var/www/backenv/bin/python',
            '/var/www/fullstack/flask/app/utils/screener_yf.py'
        ], capture_output=True, text=True, check=True)
        print(result.stdout)
        return "screener_yf Analysis script executed successfully"
    except subprocess.CalledProcessError as e:
        print(f"Error executing screener_yf Analysis script: {e}")
        print(f"Script output: {e.output}")
        return f"Error executing screener_yf Analysis script: {e}"

@celery.task
def run_rrg_data():
    try:
        result = subprocess.run([
            '/var/www/backenv/bin/python',
            '/var/www/fullstack/flask/app/utils/rrg_data.py'
        ], capture_output=True, text=True, check=True)
        print(result.stdout)
        return "rrg_data Analysis script executed successfully"
    except subprocess.CalledProcessError as e:
        print(f"Error executing rrg_data Analysis script: {e}")
        print(f"Script output: {e.output}")
        return f"Error executing rrg_data Analysis script: {e}"

@celery.task
def run_covered_call():
    try:
        result = subprocess.run([
            '/var/www/backenv/bin/python',
            '/var/www/fullstack/flask/app/utils/covered_call.py'
        ], capture_output=True, text=True, check=True)
        print(result.stdout)
        return "covered_call Analysis script executed successfully"
    except subprocess.CalledProcessError as e:
        print(f"Error executing covered_call Analysis script: {e}")
        print(f"Script output: {e.output}")
        return f"Error executing covered_call Analysis script: {e}"

@celery.task
def run_collar():
    try:
        result = subprocess.run([
            '/var/www/backenv/bin/python',
            '/var/www/fullstack/flask/app/utils/collar.py'
        ], capture_output=True, text=True, check=True)
        print(result.stdout)
        return "collar Analysis script executed successfully"
    except subprocess.CalledProcessError as e:
        print(f"Error executing collar Analysis script: {e}")
        print(f"Script output: {e.output}")
        return f"Error executing collar Analysis script: {e}"

@celery.task
def run_collar_inverted():
    try:
        result = subprocess.run([
            '/var/www/backenv/bin/python',
            '/var/www/fullstack/flask/app/utils/collar_inverted.py'
        ], capture_output=True, text=True, check=True)
        print(result.stdout)
        return "collar_inverted Analysis script executed successfully"
    except subprocess.CalledProcessError as e:
        print(f"Error executing collar_inverted Analysis script: {e}")
        print(f"Script output: {e.output}")
        return f"Error executing collar_inverted Analysis script: {e}"

@celery.task
def run_volatility_analysis():
    try:
        result = subprocess.run([
            '/var/www/backenv/bin/python',
            '/var/www/fullstack/flask/app/utils/volatility_analysis.py'
        ], capture_output=True, text=True, check=True)
        print(result.stdout)
        return "Volatility Analysis script executed successfully"
    except subprocess.CalledProcessError as e:
        print(f"Error executing Volatility Analysis script: {e}")
        print(f"Script output: {e.output}")
        return f"Error executing Volatility Analysis script: {e}"


@celery.task
def run_fetch_surface():
    try:
        result = subprocess.run([
            '/var/www/backenv/bin/python',
            '/var/www/fullstack/flask/app/utils/fetch_surface.py'
        ], capture_output=True, text=True, check=True)
        print(result.stdout)
        return "Fetch surface script executed successfully"
    except subprocess.CalledProcessError as e:
        print(f"Error executing fetch surface script: {e}")
        print(f"Script output: {e.output}")
        return f"Error executing fetch surface script: {e}"

@celery.task
def run_cointegration_matrix():
    try:
        result = subprocess.run([
            '/var/www/backenv/bin/python',
            '/var/www/fullstack/flask/app/utils/cointegration_matrix.py'
        ], capture_output=True, text=True, check=True)
        print(result.stdout)
        return "Fetch cointegration_matrix script executed successfully"
    except subprocess.CalledProcessError as e:
        print(f"Error executing fetch cointegration_matrix script: {e}")
        print(f"Script output: {e.output}")
        return f"Error executing fetch cointegration_matrix script: {e}"

@celery.task
def run_currency_cointegration_matrix():
    try:
        result = subprocess.run([
            '/var/www/backenv/bin/python',
            '/var/www/fullstack/flask/app/utils/currency_cointegration_matrix.py'
        ], capture_output=True, text=True, check=True)
        print(result.stdout)
        return "Fetch currency_cointegration_matrix script executed successfully"
    except subprocess.CalledProcessError as e:
        print(f"Error executing fetch currency_cointegration_matrix script: {e}")
        print(f"Script output: {e.output}")
        return f"Error executing fetch currency_cointegration_matrix script: {e}"


@celery.task
def run_survival_lomax():
    try:
        result = subprocess.run([
            '/var/www/backenv/bin/python',
            '/var/www/fullstack/flask/app/utils/survival_lomax.py'
        ], capture_output=True, text=True, check=True)
        print(result.stdout)
        return "Fetch survival_lomax script executed successfully"
    except subprocess.CalledProcessError as e:
        print(f"Error executing fetch survival_lomax script: {e}")
        print(f"Script output: {e.output}")
        return f"Error executing fetch survival_lomax script: {e}"


###################################################################################################################################
###################################### DOLPHINDB TASKS ############################################################################
###################################################################################################################################


@celery.task
def run_yf_historical_90m_60m_15m_5m():
    try:
        result = subprocess.run([
            '/var/www/backenv/bin/python',
            '/var/www/fullstack/dolphindb/yfs/historical_90m_60m_15m_5m.py'
        ], capture_output=True, text=True, check=True)
        print(result.stdout)
        return "Fetch Yahoo Finance historical_90m_60m_15m_5m script executed successfully"
    except subprocess.CalledProcessError as e:
        print(f"Error executing fetch Yahoo Finance historical_90m_60m_15m_5m script: {e}")
        print(f"Script output: {e.output}")
        return f"Error executing fetch Yahoo Finance historical_90m_60m_15m_5m script: {e}"

@celery.task
def run_yf_historical_1m():
    try:
        result = subprocess.run([
            '/var/www/backenv/bin/python',
            '/var/www/fullstack/dolphindb/yfs/historical_1m.py'
        ], capture_output=True, text=True, check=True)
        print(result.stdout)
        return "Fetch Yahoo Finance historical_1m script executed successfully"
    except subprocess.CalledProcessError as e:
        print(f"Error executing fetch Yahoo Finance historical_1m script: {e}")
        print(f"Script output: {e.output}")
        return f"Error executing fetch Yahoo Finance historical_1m script: {e}"

@celery.task
def run_yf_historical_1w_1d():
    try:
        result = subprocess.run([
            '/var/www/backenv/bin/python',
            '/var/www/fullstack/dolphindb/yfs/historical_1w_1d.py'
        ], capture_output=True, text=True, check=True)
        print(result.stdout)
        return "Fetch Yahoo Finance historical_1w_1d script executed successfully"
    except subprocess.CalledProcessError as e:
        print(f"Error executing fetch Yahoo Finance historical_1w_1d script: {e}")
        print(f"Script output: {e.output}")
        return f"Error executing fetch Yahoo Finance historical_1w_1d script: {e}"
