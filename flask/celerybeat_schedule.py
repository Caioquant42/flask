from celery.schedules import crontab

beat_schedule = {
    'run-ibov-stocks': {
        'task': 'app.tasks.run_ibov_stocks',
        'schedule': crontab(minute='*/5', hour='13-21', day_of_week='1-5'),
    },
    'run-fetch-surface': {
        'task': 'app.tasks.run_fetch_surface',
        'schedule': crontab(minute='*/5', hour='13-21', day_of_week='1-5'),
    },
    'run-volatility-analysis': {
        'task': 'app.tasks.run_volatility_analysis',
        'schedule': crontab(minute='*/5', hour='13-21', day_of_week='1-5'),
    },
    'run-collar-inverted': {
        'task': 'app.tasks.run_collar_inverted',
        'schedule': crontab(minute='*/5', hour='13-21', day_of_week='1-5'),
    },
    'run-covered_call': {
        'task': 'app.tasks.run_covered_call',
        'schedule': crontab(minute='*/5', hour='13-21', day_of_week='1-5'),
    },
    'run-collar': {
        'task': 'app.tasks.run_collar',
        'schedule': crontab(minute='*/5', hour='13-21', day_of_week='1-5'),
    },
    'run-cointegration-matrix': {
        'task': 'app.tasks.run_cointegration_matrix',
        'schedule': crontab(minute='0', hour='3', day_of_week='1-5'),
    },
    'run-fetch-agenda-dividendos': {
        'task': 'app.tasks.run_fetch_agenda_dividendos',
        'schedule': crontab(minute='0', hour='0', day_of_week='1-5'),
    },
    'run-statements': {
        'task': 'app.tasks.run_statements',
        'schedule': crontab(minute='0', hour='2', day_of_week='1-5'),
    },
    'run-ddm-historical-dy': {
        'task': 'app.tasks.run_ddm_historical_dy',
        'schedule': crontab(minute='0', hour='4', day_of_week='1-5'),
    },
    'run-survival-lomax': {
        'task': 'app.tasks.run_survival_lomax',
        'schedule': crontab(minute='0', hour='22', day_of_week='1-5'),
    },
    'run-screener-yf': {
        'task': 'app.tasks.run_screener_yf',
        'schedule': crontab(minute='*/5', hour='13-22', day_of_week='1-5'),
    },
    'run-fetch-br-recommendations': {
        'task': 'app.tasks.run_fetch_br_recommendations',
        'schedule': crontab(minute='0', hour='*/4', day_of_week='1-5'),
    },
    'run-fetch-nasdaq-recommendations': {
        'task': 'app.tasks.run_fetch_nasdaq_recommendations',
        'schedule': crontab(minute='0', hour='22', day_of_week='1,4'),
    },
    'run-fetch-nyse-recommendations': {
        'task': 'app.tasks.run_fetch_nyse_recommendations',
        'schedule': crontab(minute='0', hour='22', day_of_week='2,5'),
    },
    'run-yf-historical-90m-60m-15m-5m': {
        'task': 'app.tasks.run_yf_historical_90m_60m_15m_5m',
        'schedule': crontab(minute='*/30', hour='13-22', day_of_week='1-5'),
    },
    'run-yf-historical-1m': {
        'task': 'app.tasks.run_yf_historical_1m',
        'schedule': crontab(minute='0', hour='23', day_of_week='2,5'),
    },
    'run-yf-historical-1w-1d': {
        'task': 'app.tasks.run_yf_historical_1w_1d',
        'schedule': crontab(minute='0', hour='22', day_of_week='1-5'),
    },
}