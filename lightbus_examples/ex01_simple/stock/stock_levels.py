"""
A very simple web server for managing the stock levels of a companies products

"""
import sys
from uuid import uuid4

import dataset
from flask import Flask, request, redirect
import lightbus
from lightbus.utilities import configure_logging

initial_product_id = uuid4()

configure_logging()  # TODO: Sort out how we setup logging

# Setup flask and lightbus
app = Flask(__name__)
bus = lightbus.create()

# Create a simple database using the 'dataset' library
db = dataset.connect('sqlite:///stock_app.sqlite', engine_kwargs=dict(connect_args=dict(check_same_thread=False)))


@app.route('/set-stock/<product_uuid>', methods=['POST'])
def set_stock(product_uuid):
    # Insert/update the stock level in the database
    db['stock'].upsert(dict(
        uuid=product_uuid,
        quantity=int(request.form.get('quantity') or 0)
    ), keys=['uuid'])
    return redirect('/')


@app.route('/', methods=['GET'])
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


async def handle_change(**kwargs):
    products = await bus.products.all.call_async()
    db['products'].delete()
    db['products'].insert_many(products)


if __name__ == '__main__':
    if 'lightbus' in sys.argv:
        bus.products.created.listen(handle_change)
        bus.products.updated.listen(handle_change)
        bus.products.deleted.listen(handle_change)

        bus.run_forever()
    else:
        if not db['products'].count():
            db['products'].insert(dict(uuid=uuid4().hex, name='Example product'))
        app.run(port=8002, debug=True)
