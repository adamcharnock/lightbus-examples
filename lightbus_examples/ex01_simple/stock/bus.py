import lightbus

from . import db


bus = lightbus.create()


async def handle_change(**kwargs):
    products = await bus.products.all.call_async()
    db['products'].delete()
    db['products'].insert_many(products)


def before_server_start(bus):
    """
    before_server_start() within the root bus.py file
    is called before the server begins serving requests
    """
    bus.products.created.listen(handle_change)
    bus.products.updated.listen(handle_change)
    bus.products.deleted.listen(handle_change)
