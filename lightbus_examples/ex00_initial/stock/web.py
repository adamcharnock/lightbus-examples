"""
A very simple web server for managing the stock levels of a company's products

"""
import sys
from uuid import uuid4

import lightbus
from flask import Flask, request, redirect
from flask.templating import render_template

from . import db

# Create a flask webserver
web = Flask(__name__, static_folder='../../../static')


@web.route('/set-stock/<product_uuid>', methods=['POST'])
def set_stock(product_uuid):
    # Insert/update the stock level in the database
    db['stock'].upsert(dict(
        uuid=product_uuid,
        quantity=int(request.form.get('quantity') or 0)
    ), keys=['uuid'])
    return redirect('/')


@web.route('/', methods=['GET'])
def list_stock():
    return render_template('list.html',
                    products=db['products'],
                    stock=db['stock'],
    )
