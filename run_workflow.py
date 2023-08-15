from activities import log
from temporalio.client import Client
from workflow import *
import os
import asyncio

async def run_workflow():
    log("STARTING CONNECTION SERVICE WITH TEMPORAL")
    client = await Client.connect(f"{os.environ['TEMPORAL_HOST']}:{os.environ['TEMPORAL_PORT']}",namespace=os.environ['TEMPORAL_NAMESPACE'])
    log("Listing Current 'PizzahutWorkflow' Workflows")
    autoscaling_workflows = client.list_workflows("WorkflowType = 'PizzahutWorkflow'")
    handle = None
    if autoscaling_workflows:
        # Get the handle of the first running workflow
        async for autoscaling_workflow in autoscaling_workflows:
            # 1 - Running 
            # 2 - Completed
            # 3 - Failed
            # 4 - Canceled
            # 5 - Terminated
            # 6 - Continue as new
            # 7 - Timed out

            if autoscaling_workflow.status.value == 1:                
                handle = client.get_workflow_handle(workflow_id=autoscaling_workflow.id, run_id=autoscaling_workflow.run_id)                
                log(f"WORKFLOW 'PizzahutWorkflow' is already running.")

    if not handle:
        handle = await client.start_workflow(PizzahutWorkflow.run, id="PizzahutWorkflow-workflow", task_queue=os.environ['TEMPORAL_TASK_QUEUE'])            
        log(f"NEW WORKFLOW 'PizzahutWorkflow' STARTED. ")

    return await handle.result()

asyncio.run(run_workflow())
