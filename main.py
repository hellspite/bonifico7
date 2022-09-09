import deco

if __name__ == "__main__":
    month = int(input("Seleziona il mese: "))

    days = deco.get_month_days(month)

    orders = []
    for day in days:
        orders.extend(deco.get_daily_orders(day))

    # List compre
    ids = [(order["order_id"], order["billing_details"]["company"]) for order in orders]
    print(ids)
