"""
A very simple web server for managing a companies products

"""
import sys
from uuid import uuid4

from flask import Flask, request, redirect
import lightbus
from lightbus.utilities import configure_logging

configure_logging()

app = Flask(__name__)
bus = lightbus.create()

# Store the products in a simple dict indexed by UUID.
# This is simple, but we'll loose products upon restart.
products = {}


class ProductsApi(lightbus.Api):
    created = lightbus.Event(arguments=['name', 'uuid'])
    updated = lightbus.Event(arguments=['name', 'uuid'])
    deleted = lightbus.Event(arguments=['uuid'])

    class Meta:
        name = 'products'

    def all(self):
        return products


@app.route('/create', methods=['POST'])
def create_product():
    name = request.form.get('name') or 'No name'
    uuid = uuid4().hex
    products[uuid] = name
    bus.products.created.fire(name=name, uuid=uuid)
    return redirect('/')


@app.route('/delete/<uuid>', methods=['GET'])
def delete_product(uuid):
    products.pop(uuid)
    bus.products.deleted.fire(uuid=uuid)
    return redirect('/')


@app.route('/update/<uuid>', methods=['GET'])
def update_product_form(uuid):
    return """
        <h1>Update: {name}</h1>
        <form method="post" action="/update/{uuid}">
            <input type="text" name="name" placeholder="Product name" value="{name}" required>
            <input type="submit" value="Update">
        </form>
    """.format(uuid=uuid, name=products[uuid])


@app.route('/update/<uuid>', methods=['POST'])
def update_product(uuid):
    products[uuid] = request.form.get('name') or 'No name'
    bus.products.updated.fire(uuid=uuid, name=products[uuid])
    return redirect('/')


@app.route('/', methods=['GET'])
def list_products():

    product_list = [
        """
            <li>
                <a href="/update/{uuid}">{name}</a> (
                <a href="/update/{uuid}">update</a>, 
                <a href="/delete/{uuid}">delete</a>
            )</li>
        """.format(uuid=uuid, name=name)
        for uuid, name
        in products.items()
    ]
    product_list = '\n'.join(product_list) if product_list else '<li>No products, perhaps create one</li>'

    form = """
        <form method="post" action="/create">
            <input type="text" name="name" placeholder="Product name" required>
            <input type="submit" value="Create">
        </form>
    """

    return """
        <h1>Your products</h1>
        {product_list}
        <h2>Create new product</h2>
        {form}
    """.format(**locals())


if __name__ == '__main__':
    if 'lightbus' in sys.argv:
        bus.run_forever()
    else:
        app.run(port=8001, debug=True)

