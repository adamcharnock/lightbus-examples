"""
A very simple web server for managing a companies products

"""
from uuid import uuid4

from flask import Flask, request, redirect
import lightbus

from . import db

# Create a flask webserver
web = Flask(__name__)

# Create our bus
from . import bus as bus_  # Importing the API will register it with Lightbus
bus = lightbus.create()


@web.route('/create', methods=['POST'])
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


@web.route('/delete/<uuid>', methods=['GET'])
def delete_product(uuid):
    # Delete the product from our database
    db['products'].delete(dict(uuid=uuid))

    # Send lightbus 'products.deleted' event
    bus.products.deleted.fire(uuid=uuid)

    return redirect('/')


@web.route('/update/<uuid>', methods=['POST'])
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


@web.route('/update/<uuid>', methods=['GET'])
def update_product_form(uuid):
    return """
        <h1>Update: {name}</h1>
        <form method="post" action="/update/{uuid}">
            <input type="text" name="name" placeholder="Product name" value="{name}" required>
            <input type="submit" value="Update">
        </form>
    """.format(**db['products'].find_one(uuid=uuid))


@web.route('/', methods=['GET'])
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
