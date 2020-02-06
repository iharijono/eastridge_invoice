#
# File                  : db_op.py
# Date                  : 02/05/2020
# Description           : This module drives the mapping from python objects (in model.py) to the database (sqlite).
#                         It also implements DB operation (create and read) on invoice and invoice items.
#
#
# Requires              : python 3.x
#                         sqlalchemy
#
#
# Remarks               : demo code only (no production)
#
#
from db import db_session
import models
from datetime import date
import json

def add_invoice(date=date.today()):
    """ Add an invoice into the (DB) session

    :param date: date of the invoice or today if none is given
    :return: None
    """
    invoice = models.Invoice(date=date)
    db_session.add(invoice)
    db_session.commit()
    invoice_id = invoice.id
    return invoice_id


def get_invoice(invoice_id):
    """ Get the row from the database of invoice where the invoice id is 'invoice_id'

    This function is used only to ensure that the data of invoice (above) being added is persisted.
    :param invoice_id: the DB id of the invoice table
    :return: the object of invoice found in the DB or None (not found)
    """
    j_invoice = None
    invoice = db_session.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if invoice:
        j_invoice = invoice.toJSON()
        invoice_items = db_session.query(models.InvoiceItem).filter(models.InvoiceItem.invoice_id == invoice.id).all()
        j_invoice_items = [x.toJSON() for x in invoice_items]
        j_invoice["invoice_items"] = j_invoice_items
    return j_invoice


def get_all_invoices():
    """ Get all the row from the database of invoice

    This function is used only to ensure that the data of invoice (above) being added is persisted.
    :return: all object of invoice found in the DB or None (not found)
    """
    invoices = db_session.query(models.Invoice).all()
    j_invoices = None
    if invoices:
        j_invoices = []
        for invoice in invoices:
            j_invoice = invoice.toJSON()
            invoice_items = db_session.query(models.InvoiceItem).filter(models.InvoiceItem.invoice_id == invoice.id).all()
            j_invoice_items = [x.toJSON() for x in invoice_items]
            j_invoice["invoice_items"] = j_invoice_items
            j_invoices.append(j_invoice)
    return j_invoices


def add_invoice_item(units, amount, invoice_id=None, description=""):
    """ Add an invoice item into the (DB) session and link it to the (parent) invoice

    :param units: the unit of the invoice item
    :param amount: the amount of the invoice item
    :param invoice_id: the invoice, to which this invoice item belong
    :param description: the description (OPTIONAL)
    :return:
    """
    invoice_item = models.InvoiceItem(units=units, amount=amount, description=description,
                                      invoice_id = invoice_id)
    db_session.add(invoice_item)
    db_session.commit()
    invoice_item_id = invoice_item.id
    return invoice_item_id


def get_invoice_item(invoice_item_id):
    """
    Get the row from the database of invoice item where the invoice item id is 'invoice_item_id'

    This function is used only to ensure that the data of invoice item (above) being added is persisted.
    :param invoice_item_id: the DB id of the invoice item table
    :return: the object of invoice item found in the DB or None (not found)
    """
    invoice_item = db_session.query(models.InvoiceItem).filter(models.InvoiceItem.id == invoice_item_id).first()
    j_invoice_item = None
    if invoice_item:
        j_invoice_item = invoice_item.toJSON()
    return j_invoice_item


def get_all_invoice_items():
    """
    Get all the row from the database of invoice item

    This function is used only to ensure that the data of invoice item (above) being added is persisted.
    :return: all the object of invoice items found in the DB or None (not found)
    """
    invoice_items = db_session.query(models.InvoiceItem).all()
    j_invoice_items = None
    if invoice_items:
        j_invoice_items = [x.toJSON() for x in invoice_items]
    return j_invoice_items
