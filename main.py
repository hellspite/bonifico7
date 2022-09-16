from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, \
    QTableWidget, QTableWidgetItem, QHeaderView, QDesktopWidget
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

    months = deco.get_months()

    app = QApplication([])
    window = QWidget()
    window.setWindowTitle("Bonifico 7gg")
    window.setMinimumWidth(600)
    rect = window.frameGeometry()
    screen_center = QDesktopWidget().availableGeometry(window).center()
    rect.moveCenter(screen_center)
    window.move(rect.topLeft())

    layout = QVBoxLayout()
    layout.addWidget(QLabel("Ciao Marzia, seleziona il mese in cui fare la ricerca."))
    h_layout = QHBoxLayout()

    status_label = QLabel()

    cb = QComboBox()

    for month in months:
        cb.addItem(f"{MONTHS_FOR_CB[month.month]} {month.year}")

    h_layout.addWidget(cb)

    search_btn = QPushButton("Cerca")

    def search():
        print("Ricerca in corso...")
        selected_date = months[cb.currentIndex()]

        days = deco.get_month_days(selected_date.month, selected_date.year)

        status_label.setText("Ricerca in corso...")
        window.repaint()
        orders = []
        for day in days:
            orders.extend(deco.get_daily_orders(day))

        if len(orders) == 0:
            status_label.setText("Non sono stati trovati elementi")
            window.repaint()
        else:
            ids = []
            for order in orders:
                customer = ""
                if order["billing_details"]["company"] == "":
                    customer = f"{order['billing_details']['firstname']} {order['billing_details']['lastname']}"
                else:
                    customer = order["billing_details"]["company"]

                ids.append((order["order_id"], customer, order["outstanding_balance"]))

            print(ids)
            populate_table(ids)
            status_label.setText("Ricerca terminata.")
            window.repaint()


    search_btn.clicked.connect(search)

    h_layout.addWidget(search_btn)
    layout.addLayout(h_layout)

    table = QTableWidget()
    layout.addWidget(table)

    def populate_table(orders):
        rows = len(orders)
        table.setRowCount(rows)
        table.setColumnCount(3)

        for key, order in enumerate(orders):
            str_id = str(order[0])
            order_id = QTableWidgetItem(str_id)
            order_customer = QTableWidgetItem(order[1])
            outstanding_balance = QTableWidgetItem(f"{order[2]}€")

            table.setItem(key, 0, order_id)
            table.setItem(key, 1, order_customer)
            table.setItem(key, 2, outstanding_balance)

        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        table.setHorizontalHeaderLabels(["Numero Ordine", "Nome Cliente", "Da Pagare"])


    layout.addWidget(status_label)
    window.setLayout(layout)
    window.show()

    app.exec()
