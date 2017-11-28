"""
A very simple web server for managing the stock levels of a company's products

"""
import lightbus
from flask import Flask, request, redirect, render_template

from . import db

# Create a flask webserver
web = Flask(__name__, static_folder='../../../static')

# Create our bus
from . import bus as bus_  # Importing the API will register it with Lightbus
bus = lightbus.create()


@web.route('/set-stock/<product_uuid>', methods=['POST'])
def set_stock(product_uuid):
    # Insert/update the stock level in the database
    quantity = request.form.get('quantity') or 0
    db['stock'].upsert(dict(
        uuid=product_uuid,
        quantity=int(quantity)
    ), keys=['uuid'])
    return redirect('/')


@web.route('/', methods=['GET'])
def list_stock():
    return render_template('list.html',
                           products=db['products'],
                           stock=db['stock'],
    )
