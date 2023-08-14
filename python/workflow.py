from temporalio import workflow
from activities import *
from datetime import timedelta
from dataclasses import dataclass
import asyncio 


@dataclass
class Data():
    name    : str = ''
    address : str = ''
    flavor  : str = ''

@workflow.defn
class PizzahutWorkflow:
    def __init__(self) -> None:
        self._avarage_update = asyncio.Event()
        self.orders          = []
        self.order           = Data()

    async def status(self):
        log(f"Status atual: {self.statusPedido.order}")

    @workflow.run
    async def run(self) -> None:
        while True:
            log(f"WAITING FOR NEW SIGNAL...")  
            
            await asyncio.wait(
                [
                    asyncio.create_task(self._avarage_update.wait())
                ]
            )

            order = await workflow.execute_activity( 
                create_order,
                args = [self.order.name, self.order.address, self.order.flavor],
                start_to_close_timeout=timedelta(seconds=60)
            )
            await workflow.execute_activity(
                preparing_order,
                args = [order, self.order.flavor],
                start_to_close_timeout=timedelta(seconds=60)
            )
            await workflow.execute_activity(
                leave_for_delivery,
                order,
                start_to_close_timeout=timedelta(seconds=60)
            )
            log("Obrigado pelo seu pedido")

            self.order = Data()
            self._avarage_update.clear()


    # SIGNALS
    @workflow.signal
    async def new_order(self, data: Data) -> str:
        if data:
            self.orders.append(data)
            self.order.name = data.name
            self.order.address = data.address
            self.order.flavor = data.flavor

            log(f"ORDER INSERTION {self.order}")
            self._avarage_update.set()
        else:
            log(f"ORDER INVALID {data}")
    # Queries
    @workflow.query
    async def get_order_status(self):
        return self.order
    