#
# File                  : models.py
# Date                  : 02/05/2020
# Description           : This module is a simple data model for the demo.
#                         Invoice has multiple invoice items in it. So it represents one to many relationship and no invoice items
#                         can exist without its corresponding (parental) invoice.
#                         However in this implementation, there is no delete operation implemented.
#                         so if the invoice is deleted (manually), then
#                         all of its invoice items will NOT be deleted. NO CASCADE DELETE!
#
# Requires              : python 3.x
#                         sqlalchemy
#
#
# Remarks               : demo code only (no production)
#


from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from db import Base
from datetime import date

class Invoice(Base):
    # the corresponding table name in the DB
    __tablename__ = 'invoices'

    # Here we define columns for the table invoices.
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False, default=date.today())

    def __repr__(self):
        return '<Invoice(id={})>'.format(self.id)

    def toJSON(self):
        return {"id": self.id, "date": self.date}

class InvoiceItem(Base):
    # the corresponding table name in the DB
    __tablename__ = 'invoice_items'

    # Here we define columns for the table invoice_items.
    id = Column(Integer, primary_key=True, autoincrement=True)
    units = Column(Integer, default=0)
    description = Column(String(400), default="")
    amount = Column(Numeric, default=0.00)
    invoice_id = Column(Integer, ForeignKey('invoices.id'))
    invoice = relationship(Invoice)

    def __repr__(self):
        return '<InvoiceItem(id={}, units={}, amount={})>'.format(self.id, self.units, self.amount)

    def toJSON(self):
        return {"id": self.id, "units": self.units, "amount": str(round(self.amount, 2)), "description": self.description,
                "invoice_id": self.invoice_id}
