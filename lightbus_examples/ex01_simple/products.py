"""
A very simple web server for managing a companies products

"""
import sys
from uuid import uuid4

import dataset
from flask import Flask, request, redirect
import lightbus
from lightbus.utilities import configure_logging

configure_logging()  # TODO: Sort out how we setup logging

# Setup flask and lightbus
app = Flask(__name__)
bus = lightbus.create()

# Create a simple database using the 'dataset' library
db = dataset.connect('sqlite:///products_app.sqlite', engine_kwargs=dict(connect_args=dict(check_same_thread=False)))


class ProductsApi(lightbus.Api):
    created = lightbus.Event(arguments=['name', 'uuid'])
    updated = lightbus.Event(arguments=['name', 'uuid'])
    deleted = lightbus.Event(arguments=['uuid'])

    class Meta:
        name = 'products'

    def all(self):
        return [dict(product) for product in db['products'].all()]


@app.route('/create', methods=['POST'])
def create_product():
    name = request.form.get('name') or 'No name'
    uuid = uuid4().hex

    # Create product in our database
    db['products'].insert(dict(
        uuid=uuid,
        name=name,
    ))

    # Send lightbus 'products.created' event
    bus.products.created.fire(name=name, uuid=uuid)

    return redirect('/')


@app.route('/delete/<uuid>', methods=['GET'])
def delete_product(uuid):
    # Delete the product from our database
    db['products'].delete(dict(uuid=uuid))

    # Send lightbus 'products.deleted' event
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
    name = request.form.get('name') or 'No name'

    # Update the product in our database
    db['products'].update(dict(
        uuid=uuid,
        name=name,
    ), keys=['uuid'])

    # Send lightbus 'products.updated' event
    bus.products.updated.fire(uuid=uuid, name=name)

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
        """.format(**product)
        for product
        in db['products'].all()
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

