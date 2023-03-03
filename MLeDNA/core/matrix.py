import json
import xlsxwriter

def run(workdir, all_siblings_data, selected_primers, red_species, threshold_diff, uncovered_taxes):
    matrix_data = {}
    primers = []
    primers += selected_primers
    for sibling in all_siblings_data:
        primer = sibling['primer']
        tax = sibling['tax']
        if tax not in matrix_data:
            matrix_data[tax] = {}
        matrix_data[tax][primer] = sibling
        if primer not in primers:
            primers.append(primer)

    with open(f'{workdir}/matrix.json', mode='w') as out_handle:
        print(json.dumps({'primers':primers, 'selected_primers':selected_primers, \
            'red_species':list(red_species), 'matrix':matrix_data}, indent=2), file=out_handle)

    workbook = xlsxwriter.Workbook(f'{workdir}/matrix.xlsx')
    worksheet = workbook.add_worksheet('Distance Matrix')
    header_format = workbook.add_format({'bg_color': 'yellow', 'font_name': 'Arial', 'align':'center'})
    header_format.set_bold()
    body_format = workbook.add_format({'font_name': 'Arial'})
    tax_format = workbook.add_format({'font_name': 'Arial'})
    tax_format.set_bold()
    unresolved_tax_format = workbook.add_format({'bg_color': '#FADBD8', 'font_name': 'Arial'})
    unresolved_tax_format.set_bold()
    low_diff_format = workbook.add_format({'bg_color': '#FADBD8'})
    missing_format = workbook.add_format({'bg_color': '#D9D9D9'})
    headers = ['Species'] + primers
    worksheet.set_column(0,len(headers),20)
    for col in range(len(headers)):
        worksheet.write(0, col, headers[col], header_format)
    row = 1
    col = 0
    for taxID in red_species:
        if taxID in uncovered_taxes:
            worksheet.write(row, 0, taxID, unresolved_tax_format)
        else:
            worksheet.write(row, 0, taxID, tax_format)
        col = 1
        for primer in primers:
            distance = matrix_data[taxID][primer]['distance'] if primer in matrix_data[taxID] else '-'
            worksheet.write(row, col, distance, body_format)
            col += 1
        row += 1
    worksheet.conditional_format(0,0,row-1,col-1,{'type': 'cell',
                                        'criteria': '<',
                                        'value':    threshold_diff,
                                        'format':   low_diff_format})
    worksheet.conditional_format(0,0,row-1,col-1,{'type': 'cell',
                                        'criteria': '==',
                                        'value':    '"-"',
                                        'format':   missing_format})
    
    worksheet = workbook.add_worksheet('List of Siblings')
    headers = ['Primer', 'Target Species', 'Target Seq ID', 'Sibling Species', 'Sibling Seq ID', 'Distance']
    worksheet.set_column(0,len(headers)-1,20)
    for col in range(len(headers)):
        worksheet.write(0, col, headers[col], header_format)
    row = 1
    for record in matrix_data.values():
        for record_2 in record.values():
            worksheet.write(row, 0, record_2['primer'], body_format)
            worksheet.write(row, 1, record_2['tax'], body_format)
            worksheet.write(row, 2, record_2['seqid'], body_format)
            worksheet.write(row, 3, record_2['sibling_tax'], body_format)
            worksheet.write(row, 4, record_2['sibling_seqid'], body_format)
            worksheet.write(row, 5, record_2['distance'], body_format)
            row += 1
    worksheet.conditional_format(1,5,row-1,5,{'type': 'cell',
                                        'criteria': '<',
                                        'value':    threshold_diff,
                                        'format':   low_diff_format})
    
    workbook.close()