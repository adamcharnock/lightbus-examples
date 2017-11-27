from lightbus_examples.ex01_simple.stock.web import db



async def handle_change(bus, **kwargs):
    products = await bus.products.all.call_async()
    db['products'].delete()
    db['products'].insert_many(products)



def before_server_start(bus):
    bus.products.created.listen(handle_change)
    bus.products.updated.listen(handle_change)
    bus.products.deleted.listen(handle_change)
