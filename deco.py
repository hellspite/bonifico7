import requests
import os
from datetime import datetime, date, timedelta
from calendar import monthrange

USERNAME = os.environ["DECO_USER"]
PASSWORD = os.environ["DECO_PASS"]
API_URL = "https://straighttohell.eu/api/json/manage_orders/find"


def get_daily_orders(day):
    day_start_formatted = day.strftime("%Y-%m-%dT00:00:00")
    day_end_formatted = day.strftime("%Y-%m-%dT23:59:59")

    params = {
        "field": "1",
        "condition": "7",
        "date1": day_start_formatted,
        "date2": day_end_formatted,
        "sortby": 1,
        "username": USERNAME,
        "password": PASSWORD
    }

    response = requests.get(API_URL, params=params)
    bonifico7 = get_bonifico7(response.json())

    return bonifico7


# def get_weekly_priorities():
#     """Return a list of priorities for the current week
#
#     Retrieve the data of the orders from Deco API
#     """
#
#     first_day, last_day = get_days()
#
#     first_day_formatted = first_day.strftime("%Y-%m-%dT00:00:00")
#     last_day_formatted = last_day.strftime("%Y-%m-%dT00:00:00")
#
#     params = {
#         "field": "1",
#         "condition": "6",
#         "date1": first_day_formatted,
#         "sortby": 5,
#         "username": USERNAME,
#         "password": PASSWORD
#     }
#
#     response = requests.get(API_URL, params=params)
#     priorities = get_priorities(response.json())
#
#     return priorities


def get_days(month):
    """
    Returns the first, the last day of the selected month and the number of days in the month.

    :param month: the number of the month.
    :type month: int
    :return: first_day, last_day_ num_of_days
    """

    first_day = date(date.today().year, month, 1)

    num_of_days = monthrange(date.today().year, month)

    last_day = date(date.today().year, month, num_of_days[1])

    return first_day, last_day, num_of_days[1]


def get_month_days(month):
    """
    Returns a list with all the days of the selected month.

    :param month: the number of the month.
    :type month: int
    :return: month_days
    """
    first_day, last_day, num_of_days = get_days(month)

    month_days = []
    day = date(first_day.year, first_day.month, first_day.day)

    # Add all the days in a list
    for i in range(num_of_days):
        month_days.append(day)
        day = day + timedelta(1)

    return month_days


def get_bonifico7(json_response):
    """"""
    bonifico7 = []

    for order in json_response["orders"]:
        if order["account_terms"] == "Bonifico 7gg" and order["order_status"] != 7 and order["order_status"] != 4\
                and order["outstanding_balance"] > 0:
            bonifico7.append(order)

    return bonifico7
