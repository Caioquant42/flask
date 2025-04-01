from celery_worker import celery
from app.tasks import run_volatility_analysis

# Replace with your actual task ID
task_id = 'de2af953-799f-4744-8470-efe559daed25'

# Get the AsyncResult object
result = celery.AsyncResult(task_id)

# Check the task status
print("Task status:", result.status)

# Get the task result (this will wait for the task to complete if it hasn't already)
task_result = result.get()
print("Task result:", task_result)
