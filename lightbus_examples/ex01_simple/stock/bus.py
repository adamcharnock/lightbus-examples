import lightbus

from . import db


bus = lightbus.create()


async def handle_change(**kwargs):
    """Simple event handler to fetch all products upon any change"""

    # Remote procedure call to fetch all products.
    products = await bus.products.all.call_async()

    # Delete our product records and load in the newly
    # fetched records
    db['products'].delete()
    db['products'].insert_many(products)


def before_server_start(bus):
    """
    This before_server_start() hook is called before Lightbus
    begins serving requests.

    Here we setup our events listeners to deal with any product changes.
    """
    bus.products.created.listen(handle_change)
    bus.products.updated.listen(handle_change)
    bus.products.deleted.listen(handle_change)
