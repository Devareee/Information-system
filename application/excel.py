import xlsxwriter
import os

def export(rows):
    workbook = xlsxwriter.Workbook(os.path.join('diagram.xlsx'))
    worksheet = workbook.add_worksheet('sheet')

    headings = ['Город', 'Количество компаний']
    worksheet.write_row('A1', headings)

    data = [[], []]

    rows_count = len(rows)
    for row in rows:
        data[0].append(row[0])
        data[1].append(row[1])

    worksheet.write_column('A2', data[0])
    worksheet.write_column('B2', data[1])

    chart = workbook.add_chart({'type': 'pie'})
    chart.add_series({
        'categories': f'=sheet!$A$2:$A${rows_count+1}',
        'values': f'=sheet!$B$2:$B${rows_count+1}',
        'data_labels': {'percentage': True},
    })

    worksheet.set_column(1, 1, 30)
    worksheet.set_column(0, 1, 15)
    chart.set_style(10)

    worksheet.insert_chart('D1', chart)
    workbook.close()
