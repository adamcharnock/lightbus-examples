"""
A very simple web server for managing a companies products

"""
from uuid import uuid4

from flask import Flask, request, redirect, render_template
import lightbus

from . import db

# Create a flask webserver
web = Flask(__name__, static_folder='../../../static')

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
    db['products'].delete(uuid=uuid)

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
    return render_template('update.html', product=db['products'].find_one(uuid=uuid))


@web.route('/', methods=['GET'])
def list_products():
    return render_template('list.html', products=db['products'].all())

