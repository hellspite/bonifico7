from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QComboBox
import deco

MONTHS_FOR_CB = {
    1: "Gennaio",
    2: "Febbraio",
    3: "Marzo",
    4: "Aprile",
    5: "Maggio",
    6: "Giugno",
    7: "Luglio",
    8: "Agosto",
    9: "Settembre",
    10: "Ottobre",
    11: "Novembre",
    12: "Dicembre"
}

if __name__ == "__main__":
    # month = int(input("Seleziona il mese: "))
    #

    months = deco.get_months()

    app = QApplication([])
    window = QWidget()
    window.setWindowTitle("Bonifico 7gg")
    layout = QVBoxLayout()
    layout.addWidget(QLabel("Ciao Marzia, seleziona il mese in cui fare la ricerca."))

    cb = QComboBox()

    for month in months:
        cb.addItem(f"{MONTHS_FOR_CB[month.month]} {month.year}")

    layout.addWidget(cb)

    search_btn = QPushButton("Cerca")

    def search():
        print("Ricerca in corso...")
        selected_date = months[cb.currentIndex()]

        days = deco.get_month_days(selected_date.month, selected_date.year)

        orders = []
        for day in days:
            orders.extend(deco.get_daily_orders(day))

        # List comprehension
        ids = [(order["order_id"], order["billing_details"]["company"]) for order in orders]
        print(ids)

    search_btn.clicked.connect(search)

    layout.addWidget(search_btn)
    window.setLayout(layout)
    window.show()

    # TODO: Create table with results

    app.exec()
