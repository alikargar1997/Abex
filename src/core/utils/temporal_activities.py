from temporalio import workflow
from datetime import timedelta
from functools import partial

execute_activity = partial(
    workflow.execute_activity, start_to_close_timeout=timedelta(minutes=1)
)
