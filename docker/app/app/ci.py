#! /usr/bin/python
"""
    codeship-build-check.py
    -------------------

    The purpose of this script to run as a regression
    script to test the project docker build.

"""
import os
import sys
import psycopg2


def database_check():
    try:
        psycopg2.connect(
            dbname=os.environ.get('POSTGRES_NAME'),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD'),
            host=os.environ.get('POSTGRES_HOST'),
            port=os.environ.get('POSTGRES_PORT'))
    except:
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    database_check()
