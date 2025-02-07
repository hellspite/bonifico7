from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, \
    QListWidget, QTableWidget, QTableWidgetItem, QHeaderView, QDesktopWidget, QFileDialog, QAbstractItemView

import deco
from excel import populate_excel
from datetime import datetime, date, timedelta

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

PAYMENT_METHODS = [
    "* Bonifico 30gg",
    "* Bonifico 60gg",
    "* Ri.ba. 30gg f.m.",
    "* Ri.Ba. 60gg f.m.",
    "* Ri.Ba. 90gg f.m.",
    "* Ri.Ba. 60+90gg f.m.",
    "* Anticipo 50% e saldo prima della consegna",
    "** Rimessa Diretta",
    "* Bonifico 120gg f.m.",
    "* Anticipo 50%, Saldo Ri.Ba. 30gg",
    "* A Vista Fattura",
    "Acconto 30%, Saldo 35% Ri.Ba. 30gg, 35% Ri.Ba. 60gg",
    "* Acconto 40%, Saldo Ri.Ba. a 30 gg fm",
    "* Anticipo 50%, Saldo bonifico 30 gg fm",
    "Acconto 20%, 2° acconto 20%, saldo Ri.ba 30 gg fm",
    "ACCONTO 40% - SALDO 30% A 30 GG - 30% A 60 GG",
    "* Anticipo 40%, Saldo bonifico 30 gg df",
    "* Bonifico 60+90gg f.m."
]

if __name__ == "__main__":

    orders_to_print = []

    months = deco.get_months()
    print(months)

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

    cbm = QComboBox()
    cby = QComboBox()

    for month in MONTHS_FOR_CB:
        cbm.addItem(MONTHS_FOR_CB[month])

    cbm.setCurrentText(f"{MONTHS_FOR_CB[months[-1].month]}")

    for i in range(5):
        decrease = 5
        decrease -= i

        current_year = datetime.now().year
        year = current_year - decrease
        cby.addItem(str(year))
        if i == 4:
            cby.addItem(str(current_year))

    cby.setCurrentText(f"{datetime.now().year}")

    h_layout.addWidget(cbm)
    h_layout.addWidget(cby)

    ql_payment = QListWidget()

    ql_payment.setSelectionMode(QAbstractItemView.ExtendedSelection)
    ql_payment.setAlternatingRowColors(True)
    ql_payment.setMaximumHeight(100)

    for method in PAYMENT_METHODS:
        ql_payment.addItem(method)

    h_layout.addWidget(ql_payment)

    search_btn = QPushButton("Cerca")

    def search():
        # if there's a table, clean it
        if table:
            while table.rowCount() > 0:
                table.removeRow(0)
            window.repaint()

        global orders_to_print
        print("Ricerca in corso...")
        year = int(cby.currentText())
        month = cbm.currentIndex() + 1

        selected_date = date(year, month, 1)
        current_month = date(datetime.now().year, datetime.now().month, 1)

        if selected_date > current_month:
            status_label.setText("La data selezionata non è corretta!")
            window.repaint()
            return

        selected_list_items = ql_payment.selectedItems()

        selected_payments = []
        for item in selected_list_items:
            selected_payments.append(item.text())

        days = deco.get_month_days(month, year)

        status_label.setText("Ricerca in corso...")
        window.repaint()
        orders = []
        for day in days:
            orders.extend(deco.get_daily_orders(day, selected_payments))

        if len(orders) == 0:
            status_label.setText("Non sono stati trovati elementi.")
            window.repaint()
        else:
            ids = []
            for order in orders:
                customer = ""
                if order["billing_details"]["company"] == "":
                    customer = f"{order['billing_details']['firstname']} {order['billing_details']['lastname']}"
                else:
                    customer = order["billing_details"]["company"]

                ids.append((order["order_id"], customer, order["outstanding_balance"], order["account_terms"]))

            print(ids)
            orders_to_print = ids
            populate_table(ids)
            status_label.setText("Ricerca terminata.")
            window.repaint()


    search_btn.clicked.connect(search)

    export_btn = QPushButton("Esporta in excel")


    def export_excel():
        global orders_to_print

        if not orders_to_print:
            status_label.setText("Non ci sono ordini da esportare!")
        else:
            name = QFileDialog.getSaveFileName(filter="Excel (*.xlsx)")
            filename = name[0]
            if filename[-5:] != ".xlsx":
                filename += ".xlsx"
            populate_excel(filename, orders_to_print)
            status_label.setText("Ordini esportati correttamente.")

        window.repaint()

    export_btn.clicked.connect(export_excel)

    h_layout.addWidget(search_btn)
    h_layout.addWidget(export_btn)
    layout.addLayout(h_layout)

    table = QTableWidget()
    layout.addWidget(table)

    def populate_table(orders):
        rows = len(orders)
        table.setRowCount(rows)
        table.setColumnCount(4)

        for key, order in enumerate(orders):
            str_id = str(order[0])
            order_id = QTableWidgetItem(str_id)
            order_customer = QTableWidgetItem(order[1])
            outstanding_balance = QTableWidgetItem(f"€{order[2]}")
            payment = QTableWidgetItem(order[3])

            table.setItem(key, 0, order_id)
            table.setItem(key, 1, order_customer)
            table.setItem(key, 2, outstanding_balance)
            table.setItem(key, 3, payment)

        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        table.setHorizontalHeaderLabels(["Numero Ordine", "Nome Cliente", "Da Pagare", "Metodo di Pagamento"])


    layout.addWidget(status_label)
    window.setLayout(layout)
    window.show()

    app.exec()
