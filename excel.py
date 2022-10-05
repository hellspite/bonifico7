import xlsxwriter


def populate_excel(name, orders):
    workbook = xlsxwriter.Workbook(name)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({"bold": True})
    worksheet.write("A1", "Numero Ordine", bold)
    worksheet.write("B1", "Nome Cliente", bold)
    worksheet.write("C1", "Da Pagare", bold)
    worksheet.set_column("A:A", 15)
    worksheet.set_column("B:B", 18)
    worksheet.set_column("C:C", 12)

    row = 1
    col = 0

    for order in orders:
        worksheet.write(row, col, order[0])
        worksheet.write(row, col+1, order[1])
        worksheet.write(row, col+2, f"€{order[2]}")

        row += 1

    workbook.close()
