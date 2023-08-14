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
        time.sleep(int(os.environ['SLEEP']))
        return arraydados
    else:
        log("NUMBER ODD "+ str(order))
        raise ValueError("order must be pair")


@activity.defn
async def preparing_order(order, flavor):
    time.sleep(int(os.environ['SLEEP']))
    log(f"Your order number {order} ({flavor} pizza) has already been prepared!")
    return  f"Your order number {order} ({flavor} pizza) has already been prepared!"

@activity.defn
async def leave_for_delivery(order):
    time.sleep(int(os.environ['SLEEP']))
    log(f"Your order number {order} is out for delivery!")
    return f"Your order number {order} is out for delivery!"
