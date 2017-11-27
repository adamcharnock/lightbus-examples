"""
A very simple web server for managing the stock levels of a companies products

"""
import sys
from uuid import uuid4

import lightbus
from flask import Flask, request, redirect

from . import db

# Create a flask webserver
web = Flask(__name__)

# Create our bus
from . import bus as bus_  # Importing the API will register it with Lightbus
bus = lightbus.create()


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

    stock_list = []

    for product in db['products'].all():
        stock_record = db['stock'].find_one(uuid=product['uuid'])
        stock_list.append("""
            <tr>
                <td>{name}</td>
                <td>
                    <form method="post" action="/set-stock/{uuid}">
                        <input type="number" name="quantity" value="{stock}" required>
                        <input type="submit" value="Update">
                    </form>
                </td>
            </tr>
            """.format(
                stock=stock_record['quantity'] if stock_record else 0,
                **product,
            )
        )

    if not stock_list:
        stock_list = """<tr><td colspan="2">No products found</td></tr>"""
    else:
        stock_list = ''.join(stock_list)

    return """
    <h1>Stock levels</h1>
    <table>
        <tr>
            <th width="400">Product name</th>
            <th>Stock level</th>
        </tr>
        {stock_list}
    </table>
    """.format(**locals())
