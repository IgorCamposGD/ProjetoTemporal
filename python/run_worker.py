from temporalio.client import Client
from temporalio.worker import Worker
import os
from workflow import PizzahutWorkflow
from activities import *
import asyncio


async def run_worker():    
    log("STARTING WORKER ON WORKFLOW")

    client = await Client.connect(f"{os.getenv('TEMPORAL_HOST')}:{os.getenv('TEMPORAL_PORT')}",namespace=os.getenv('TEMPORAL_NAMESPACE'))

    #Run a worker for the workflow
    worker = Worker(
        client,
        task_queue=os.getenv('TEMPORAL_TASK_QUEUE'),
        workflows = [PizzahutWorkflow],
        activities = [create_order,preparing_order,leave_for_delivery],
    )
    log("WORKER STARTED.")
    await worker.run()

asyncio.run(run_worker())