import xlsxwriter


def populate_excel(name, orders):
    workbook = xlsxwriter.Workbook(name)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({"bold": True})
    worksheet.write("A1", "Numero Ordine", bold)
    worksheet.write("B1", "Nome Cliente", bold)
    worksheet.write("C1", "Da Pagare", bold)
    worksheet.write("D1", "Metodo di Pagamento", bold)
    worksheet.write("E1", "Fattura", bold)
    worksheet.write("F1", "Spedizione", bold)
    worksheet.set_column("A:A", 15)
    worksheet.set_column("B:B", 18)
    worksheet.set_column("C:C", 12)
    worksheet.set_column("D:D", 16)
    worksheet.set_column("E:E", 14)
    worksheet.set_column("F:F", 14)

    row = 1
    col = 0

    for order in orders:
        worksheet.write(row, col, order[0])
        worksheet.write(row, col+1, order[1])
        worksheet.write(row, col+2, f"€{order[2]}")
        worksheet.write(row, col+3, order[3])
        worksheet.write(row, col+4, order[4])
        worksheet.write(row, col+5, order[5])

        row += 1

    workbook.close()
