from temporalio import activity
import random
import logging
import time
import os




# Log config
logger = logging.getLogger('pizzahut')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def log(msg,level='info'):
    # 'application' code
    if level == 'debug':
        return logger.debug(msg)
    if level == 'info':
        return logger.info(msg)
    if level == 'warning':
        return logger.warning(msg)
    if level == 'error':
        return logger.error(msg)
    if level == 'critical':
        return logger.critical(msg)


#General activities
@activity.defn
async def create_order(name, address, flavor):

    order = random.randint(1000, 9999)

    if order % 2 == 0:
        arraydados = {"order": order, "name": name, "adress": address, "flavor": flavor, "status":"order_created"}
        log(arraydados)
        return arraydados
    else:
        log("NUMBER ODD "+ str(order))
        raise ValueError("order must be pair")


@activity.defn
async def preparing_order(order, flavor):
    order_id = order['order']
    order['status'] = "preparing_order"
    time.sleep(int(os.environ['SLEEP']))
    log(f"Your order number {order_id} ({flavor} pizza) has already been prepared!")
    return  order

@activity.defn
async def leave_for_delivery(order):
    order_id = order['order']
    order['status'] = "out_of_delivery"
    time.sleep(int(os.environ['SLEEP']))
    log(f"Your order number {order_id} is out for delivery!")
    return order
