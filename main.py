#!/usr/bin/env python
#
# File                  : main.py
# Date                  : 02/05/2020
# Description           : main (driver) application for invoices
#                         this application
#
#
# Requires              : python 3.x
#                         flask
#                         sqlalchemy
#
#
# Remarks               : demo code only (no production)
#
from api import init_api
from db import init_db

DEFAULT_PORT = 9000
LOWEST_PORT_NUMBER = 2000
def get_valid_port(port_nr):
    """
    Check the validity of a port number given, if it is valid, return the port number in integer
    Port is valid if it is positive number greater than 2000 (port number 2000 usually is reserved for super user processes).
    if invalid, Here we can either throw an exception or 'silently' reset the port number into valid number (e.g. 9000), but
    I prefer the first option because it is explicit

    :param port_nr: port number
    :return: port number
    :exception: ValueError exception is thrown if the port_nr is the integer value less than 2000
    """
    if port_nr <= LOWEST_PORT_NUMBER:
        raise ValueError("Port number given '{}' is less than {}".format(port_nr, LOWEST_PORT_NUMBER))
    return port_nr

def run(port=DEFAULT_PORT, verbose=False):
    """
    the main driver for the application.
    It initializes everything (Flask, DB etc.)

    :param port: the port number
    :param verbose: print out debugging message or not
    :return:
    """
    init_db()
    init_api(port = port, debug=verbose)

if __name__ == "__main__":
    import argparse

    PORT = DEFAULT_PORT
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default = DEFAULT_PORT,
                        help="port on which the service is listening for incoming (REST API) request, default ({})"
                        .format(DEFAULT_PORT))
    parser.add_argument("-v", "--verbose", default = False, action='store_true',
                        help="print all incoming (REST API) request and outgoing response")
    args = parser.parse_args()
    if args.port:
        try:
            PORT = get_valid_port(args.port)
        except ValueError as err:
            print(err)
            exit(-1)
    run(PORT, args.verbose)