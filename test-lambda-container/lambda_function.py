import logging
import sys


def three():
    print("three")
    raise Exception('This is an exception from Python!')


def two():
    print("two")
    three()


def one():
    print("one")
    two()


def handler(event, context):
    print("I am here!")
    one()
    return f'Servus from AWS Lambda using Python {sys.version}! (event: {event})'
