#
# File                  : api.py
# Date                  : 02/05/2020
# Description           : main REST API for invoices
#
#
#
# Requires              : python 3.x
#                         flask
#                         db
#
#
# Remarks               : demo code only (no production)
#

from db import stop_db
from db_op import add_invoice, get_invoice, get_all_invoices, add_invoice_item, get_invoice_item, get_all_invoice_items
from flask import Flask, request, abort, jsonify, make_response
from datetime import date, datetime

app = Flask(__name__)

@app.errorhandler(422)
def not_processable(error):
    return make_response(jsonify({'error': 'Unprocessable Entity, wrong/missing parameter'}), 422)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def format_err(error):
    return make_response(jsonify({'error': 'Must be json formatted data'}), 400)


@app.route('/invoices', methods=['POST'])
def create_invoice():
    """
    The REST API to create an invoice

    if date is specified, the invoice is created with the date, otherwise today's date is taken
    :return: json formatted response containing the (unique) id of the invoice
    """
    inv_date = date.today()
    if 'date' in request.json:
        inv_date_str = request.json['date']
        inv_date = datetime.strptime(inv_date_str, '%Y-%m-%d').date()

    # db operation
    invoice_id = add_invoice(inv_date)
    return jsonify({'invoice_id': invoice_id}), 201


@app.route('/invoices/<int:invoice_id>', methods=['GET'])
def get_inv(invoice_id):
    invoice = get_invoice(invoice_id)
    if not invoice:
        abort(404)
    return jsonify(invoice), 200

@app.route('/invoices', methods=['GET'])
def get_all_invoice():
    """
    The REST API to get all invoices

    :return: json formatted response containing all the invoices
    """
    # db operation
    invoices = get_all_invoices()
    return jsonify(invoices), 200


@app.route('/invoice_items', methods=['POST'])
def create_invoice_item():
    """
    The REST API to create an invoice item

    if date is specified, the invoice is created with the date, otherwise today's date is taken
    :return: json formatted response containing the (unique) id of the invoice item
    """
    if not request.json:
        abort(400)
    description = ""
    invoice_id = None
    if 'units' in request.json:
        units = int(request.json['units'])
    if 'amount' in request.json:
        amount = float(request.json['amount'])
    if 'description' in request.json:
        description = request.json['description']
    if 'invoice_id' not in request.json:
        abort(422)
    else:
        invoice_id = int(request.json['invoice_id'])
    invoice = get_invoice(invoice_id)
    if not invoice:
        abort(422)

    # db operation
    invoice_item_id = add_invoice_item(units=units, amount=amount, description=description, invoice_id=invoice_id)
    return jsonify({'invoice_item_id': invoice_item_id}), 201


@app.route('/invoice_items/<int:invoice_item_id>', methods=['GET'])
def get_inv_item(invoice_item_id):
    invoice_item = get_invoice_item(invoice_item_id)
    if not invoice_item:
        abort(404)
    return jsonify(invoice_item), 200


@app.route('/invoice_items', methods=['GET'])
def get_all_invoice_items():
    """
    The REST API to get all invoice items

    :return: json formatted response containing all the invoice items
    """
    # db operation
    invoice_items = get_all_invoice_items()
    return jsonify(invoice_items), 200


# The DB session is automatically destroyed when the app exits
@app.teardown_appcontext
def shutdown_session(exception=None):
    stop_db()

def init_api(host='localhost', port=9000, debug=False):
    """
    Start the Flask API process

    :param host: host where Flask is listening for the API request calls
    :param port: the port number where Flask is listening for the API request calls
    :param debug: print the output or not when a request is coming
    :return: None
    """
    app.run(host=host, port=port, debug=debug)


