from lightbus import Api, Event

from . import db


class ProductsApi(Api):
    created = Event(arguments=['name', 'uuid'])
    updated = Event(arguments=['name', 'uuid'])
    deleted = Event(arguments=['uuid'])

    class Meta:
        # The name below defines how this api will be accessed,
        # eg: bus.products.all()
        name = 'products'

    def all(self):
        """Get all products"""

        # The database returns OrderdDict objects, convert them into
        # regular dicts so they can be easily serialised.
        return [dict(product) for product in db['products'].all()]
