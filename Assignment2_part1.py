import argparse
import urllib.request
import logging
import datetime


def downloadData(url):
    """Reads data from a local file specified by the URL."""
    try:
        with open(url, 'r') as file:
            data = file.read()
        return data
    except Exception as e:
        print("Error reading data from file:", str(e))
        exit(1)
