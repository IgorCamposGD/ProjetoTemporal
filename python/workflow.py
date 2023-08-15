from temporalio import workflow
from activities import *
from datetime import timedelta
from dataclasses import dataclass
import asyncio


@dataclass
class Data:
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

            self.orders.append(order)

            order = await workflow.execute_activity(
                preparing_order,
                args = [order, self.order.flavor],
                start_to_close_timeout=timedelta(seconds=60)
            )

            for i in self.orders:
                if i['order'] == order['order']:
                    i['status'] = order['status']

            order = await workflow.execute_activity(
                leave_for_delivery,
                order,
                start_to_close_timeout=timedelta(seconds=60)
            )

            for i in self.orders:
                if i['order'] == order['order']:
                    i['status'] = order['status']

            log(f"Pedidos {order}")

            self.order = Data()
            self._avarage_update.clear()


    # SIGNALS
    @workflow.signal
    async def new_order(self, data: Data) -> str:
        if data:

            if data.name and data.address not in {''}:
                self.order.name = data.name
                self.order.address = data.address
            else:
                log("A variável NAME ou ADDRESS não podem ser vazia")

            if data.flavor not in {'Frango','Calabresa','Chocolate'}:
                log("A variável FLAVOR deve ter um dos valores: 'Frango','Calabresa','Chocolate'")
            else:
                self.order.flavor = data.flavor
        
            if self.order.name and self.order.address and self.order.flavor not in {''}:
                log(f"ORDER INSERTION {self.order}")
                self._avarage_update.set()
            else:
                log("ORDER CANCELED DUE TO LACK OF DATA")

        else:
            log(f"ORDER INVALID {data}")

    @workflow.signal
    async def confirm_delivery(self, order_id):
        if order_id:
            for i in self.orders:
                if order_id == i['order'] and i['status'] == 'out_of_delivery':
                    i['status'] = "delivery"
                    log("Out for delivery")
                else:
                    log("Order not ready for delivery yet")
        else:
            log("Inform order number")

    @workflow.query
    async def orders_list(self, comando):
        if comando:
            return self.orders
        
    # Queries
    @workflow.query
    async def get_order_status(self, order_id) -> dict:
        for i in self.orders:
            if order_id == i['order']:
                log("ID FOUND")
                return i
            else:
                log("looking for number")
        return {"status":"order not found"}
