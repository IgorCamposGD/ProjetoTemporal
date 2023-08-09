import asyncio
import os
from temporalio.client import Client
from temporalio import workflow, activity
import json

@activity.defn
async def digite_nome():

    while True:
        nome = input("Digite seu nome: ")

        if nome == '':
            print("Campo não pode estar vazio!")
        else:
            return nome


@activity.defn
async def digite_endereco():
    while True:
        endereco = input("Digite seu endereco: ")

        if endereco == "":
            print("Campo não pode estar vazio!")
        else:
            return endereco
        
@activity.defn
def digite_sabor():

    sabores = os.getenv('PIZZA_SABORES')
    sabores = sabores.split(', ')

    while True:
        print(f"Menu de sabores de hoje: {sabores}")
        sabor = input("Digite um dos sabores: ")

        if sabor == "":
            print("Campo não pode estar vazio!")
        else:
            index = 0
            totalSabores = len(sabores)
            for i in sabores:
                index = index + 1
                if sabor != i:
                    if totalSabores == index:                    
                        print("Sabor discado não está no menu de hoje, Digite um sabor das opções do menu!")
                else:
                    return sabor


@workflow.defn
class PizzahutWorkflow:
    @workflow.run
    async def run(self):

        await workflow.execute_activity(
            name = await digite_nome()
        )
        await workflow.execute_activity(
            digite_endereco
        )
        await workflow.execute_activity(
            digite_sabor
        )


        return {"msg": f"Pedido de pizza sabor  do cliente  de endereco  registrado!"}

async def start_temporal():
    #Start client
    print(f"{os.getenv('TEMPORAL_HOST')}:{os.getenv('TEMPORAL_PORT')}")
    client = await Client.connect(f"{os.getenv('TEMPORAL_HOST')}:{os.getenv('TEMPORAL_PORT')}",namespace=os.getenv('TEMPORAL_NAMESPACE'))
    #Run a worker for the workflow
    worker = Worker(
        client,
        task_queue=os.getenv('TEMPORAL_TASK_QUEUE'),
        workflows = [PizzahutWorkflow],
        activities = [digite_nome, digite_endereco, digite_sabor],
    )

    await worker.run()

if __name__ == "__main__":
    asyncio.run(start_temporal())