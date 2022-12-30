import requests
import os
from datetime import date, timedelta
from calendar import monthrange

USERNAME = os.environ["DECO_USER"]
PASSWORD = os.environ["DECO_PASS"]
API_URL = "https://straighttohell.eu/api/json/manage_orders/find"


def get_months():
    today = date.today()
    first_month = date(today.year - 1, today.month, 1)

    months = [first_month]
    month = first_month
    for i in range(12):
        if month.month == 12:
            next_month = date(month.year + 1, 1, 1)
        else:
            next_month = date(month.year, month.month + 1, 1)
        months.append(next_month)
        month = next_month

    return months


def get_daily_orders(day, payments):
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
    bonifico7 = get_bonifico7(response.json(), payments)

    return bonifico7


def get_days(month, year):
    """
    Returns the first, the last day of the selected month and the number of days in the month.

    :param month: the number of the month.
    :type month: int
    :param year: the number of the year.
    :type year: int
    :return: first_day, last_day_ num_of_days
    """

    first_day = date(year, month, 1)

    num_of_days = monthrange(date.today().year, month)

    last_day = date(year, month, num_of_days[1])

    return first_day, last_day, num_of_days[1]


def get_month_days(month, year):
    """
    Returns a list with all the days of the selected month.

    :param month: the number of the month.
    :type month: int
    :param year: the number of the year
    :type year: int
    :return: month_days
    """
    first_day, last_day, num_of_days = get_days(month, year)

    month_days = []
    day = date(first_day.year, first_day.month, first_day.day)

    # Add all the days in a list
    for i in range(num_of_days):
        month_days.append(day)
        day = day + timedelta(1)

    return month_days


def get_bonifico7(json_response, payments):
    """"""
    bonifico7 = []

    for order in json_response["orders"]:
        if order["account_terms"] in payments:
            if order["order_status"] != 7 and order["order_status"] != 4 and order["outstanding_balance"] > 0:
                bonifico7.append(order)

    return bonifico7
