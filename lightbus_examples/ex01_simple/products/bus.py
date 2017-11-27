import lightbus

from . import db


class ProductsApi(lightbus.Api):
    created = lightbus.Event(arguments=['name', 'uuid'])
    updated = lightbus.Event(arguments=['name', 'uuid'])
    deleted = lightbus.Event(arguments=['uuid'])

    class Meta:
        name = 'products'

    def all(self):
        return [dict(product) for product in db['products'].all()]
