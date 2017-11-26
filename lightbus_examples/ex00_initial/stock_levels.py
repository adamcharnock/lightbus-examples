"""
A very simple web server for managing the stock levels of a companies products

"""
from uuid import uuid4

from flask import Flask, request, redirect

initial_product_id = uuid4().hex

# Store the stock levels & products in simple dicts indexed by product UUID.
# This is simple, but we'll loose stock data upon restart.
stock_levels = {
    initial_product_id: 5,
}
products = {
    initial_product_id: "Demo initial product"
}

app = Flask(__name__)


@app.route('/set-stock/<product_uuid>', methods=['POST'])
def set_stock(product_uuid):
    stock_levels[product_uuid] = int(request.form.get('quantity') or 0)
    return redirect('/')


@app.route('/', methods=['GET'])
def list_stock():

    stock_list = []

    for uuid in products.keys():
        stock_list.append("""
            <tr>
                <td>{name}</td>
                <td>
                    <form method="post" action="/set-stock/{product_uuid}">
                        <input type="number" name="quantity" value="{stock_level}" required>
                        <input type="submit" value="Update">
                    </form>
                </td>
            </tr>
            """.format(
                name=products[uuid],
                stock_level=stock_levels.get(uuid, 0),
                product_uuid=uuid,
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


if __name__ == '__main__':
    app.run(port=8002, debug=True)

