"""Provide user defined Links

Provide User defined Links to external providers for Charts and Trading
"""

import json
import time
import requests


def get_trading_link(isin: str):
    """
    Return a link to a trading website, based on provided ISIN

    Args:
        isin (str): ISIN to create the link for

    Todo:
        Implement userspecific part

    Returns:
        str: Link to trading platform for provided ISIN
    """
    trading_url = None
    #if isin:
        #put your implementation here
    return trading_url


def get_chart_link(isin: str):
    """
    Return a link to external chart provider, based on provided ISIN

    Args:
        isin (str): ISIN to create the link for

    Todo:
        Implement userspecific part

    Returns:
        str: Link to chart for provided ISIN
    """
    chart_info = None
    #if isin:
        #put your implementation here
    return chart_info
